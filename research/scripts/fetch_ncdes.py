#!/usr/bin/env python3
"""Resolve and ingest practice-level Network Contract DES data.

NHS England publishes one cumulative extract per financial-year month at an
opaque files.digital.nhs.uk URL. This script resolves the publication pages,
records exact source URLs and hashes, downloads each distinct data dictionary,
and can build a filtered practice-month long table without committing the raw
ZIP archives.

The source values are retained as published. In particular, monthly extracts
are cumulative from 1 April and must not be interpreted as monthly activity.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path

import duckdb
import pandas as pd


SERIES_URL = (
    "https://digital.nhs.uk/data-and-information/publications/statistical/"
    "mi-network-contract-des"
)
MONTH_NUMBERS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}
USER_AGENT = "gp-oc-dashboard-ncdes-ingestion/1.0"


class AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[dict[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self._href = href
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            self.anchors.append(
                {
                    "href": self._href,
                    "text": " ".join(" ".join(self._text).split()),
                }
            )
            self._href = None
            self._text = []


def fetch_bytes(url: str, attempts: int = 4) -> bytes:
    error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.read()
        except Exception as exc:  # pragma: no cover - network failure path
            error = exc
            if attempt + 1 < attempts:
                time.sleep(2**attempt)
    raise RuntimeError(f"Unable to fetch {url}: {error}")


def anchors(url: str) -> list[dict[str, str]]:
    parser = AnchorParser()
    parser.feed(fetch_bytes(url).decode("utf-8", errors="replace"))
    return parser.anchors


def period_from_publication_url(url: str) -> str | None:
    match = re.search(r"/england-([a-z]+)-(20\d{2})(?:/|$)", url.lower())
    if not match or match.group(1) not in MONTH_NUMBERS:
        return None
    return f"{match.group(2)}{MONTH_NUMBERS[match.group(1)]:02d}"


def discover_publication_pages(from_period: str, to_period: str | None) -> list[dict[str, str]]:
    found: dict[str, str] = {}
    for anchor in anchors(SERIES_URL):
        url = urllib.parse.urljoin(SERIES_URL, anchor["href"])
        period = period_from_publication_url(url)
        if period is None or period < from_period or (to_period and period > to_period):
            continue
        # A handful of pages use a trailing /content-copy path. Keep the exact live link.
        found[period] = url
    return [{"period": period, "page_url": found[period]} for period in sorted(found)]


def resolve_publication(row: dict[str, str]) -> dict[str, str]:
    resources = anchors(row["page_url"])
    data_candidates = []
    dictionary_candidates = []
    for resource in resources:
        url = urllib.parse.urljoin(row["page_url"], resource["href"])
        text = resource["text"].lower()
        clean_url = url.split("?", 1)[0].lower()
        # At least one historic page (July 2023) has the two human-readable
        # resource labels reversed. The file names correctly identify the
        # multi-file by-ruleset archive, so select on the URL as well as text.
        if (
            clean_url.endswith(".zip")
            and "network contract des" in text
            and "by_ruleset" not in clean_url
        ):
            data_candidates.append(url)
        if clean_url.endswith(".xlsx") and "data dictionary" in text:
            dictionary_candidates.append(url)
    if len(set(data_candidates)) != 1:
        raise RuntimeError(
            f"Expected one complete-data ZIP on {row['page_url']}; found {data_candidates}"
        )
    if not dictionary_candidates:
        raise RuntimeError(f"No data dictionary found on {row['page_url']}")
    # When a page retains superseded resources, the final linked dictionary is current.
    resolved = dict(row)
    resolved["data_url"] = data_candidates[-1]
    resolved["dictionary_url"] = dictionary_candidates[-1]
    return resolved


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, directory: Path, filename: str | None = None) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    name = filename or (
        hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
        + "__"
        + urllib.parse.unquote(Path(urllib.parse.urlparse(url).path).name)
    )
    path = directory / name
    if not path.exists():
        path.write_bytes(fetch_bytes(url))
    return path


def build_dictionary_catalogs(
    releases: list[dict[str, str]],
    dictionary_dir: Path,
    indicator_output_path: Path,
    measure_output_path: Path,
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, dict[str, str]]]:
    dictionary_periods: dict[str, list[str]] = {}
    for release in releases:
        dictionary_periods.setdefault(release["dictionary_url"], []).append(release["period"])

    indicator_catalog: list[dict[str, str]] = []
    measure_catalog: list[dict[str, str]] = []
    dictionary_files: dict[str, dict[str, str]] = {}
    for url, periods in sorted(dictionary_periods.items(), key=lambda item: min(item[1])):
        path = download(url, dictionary_dir)
        dictionary_files[url] = {"path": str(path), "sha256": sha256(path)}
        frame = pd.read_excel(path, sheet_name="Indicators", dtype=str).fillna("")
        required = {
            "YEAR",
            "QUALITY_SERVICE",
            "INDICATOR_ID",
            "INDICATOR_DESCRIPTION",
            "RULESET_ID",
            "INDICATOR_TYPE",
        }
        if not required.issubset(frame.columns):
            raise RuntimeError(f"Unexpected Indicators sheet in {path}: {list(frame.columns)}")
        for record in frame.to_dict(orient="records"):
            if not str(record["INDICATOR_ID"]).strip():
                continue
            indicator_catalog.append(
                {
                    "dictionary_file": path.name,
                    "dictionary_sha256": sha256(path),
                    "dictionary_url": url,
                    "first_release_period": min(periods),
                    "last_release_period": max(periods),
                    **{column: str(record[column]).strip() for column in required},
                }
            )

        measures = pd.read_excel(path, sheet_name="Measures", dtype=str).fillna("")
        measure_required = {"MEASURE", "MEASURE_DESCRIPTION", "MEASURE_TYPE"}
        if not measure_required.issubset(measures.columns):
            raise RuntimeError(f"Unexpected Measures sheet in {path}: {list(measures.columns)}")
        for record in measures.to_dict(orient="records"):
            if not str(record["MEASURE"]).strip():
                continue
            measure_catalog.append(
                {
                    "dictionary_file": path.name,
                    "dictionary_sha256": sha256(path),
                    "dictionary_url": url,
                    "first_release_period": min(periods),
                    "last_release_period": max(periods),
                    **{
                        column: str(record[column]).strip()
                        for column in measure_required
                    },
                }
            )

    fields = [
        "dictionary_file",
        "dictionary_sha256",
        "dictionary_url",
        "first_release_period",
        "last_release_period",
        "YEAR",
        "QUALITY_SERVICE",
        "INDICATOR_ID",
        "INDICATOR_DESCRIPTION",
        "RULESET_ID",
        "INDICATOR_TYPE",
    ]
    indicator_output_path.parent.mkdir(parents=True, exist_ok=True)
    with indicator_output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(indicator_catalog)

    measure_fields = [
        "dictionary_file",
        "dictionary_sha256",
        "dictionary_url",
        "first_release_period",
        "last_release_period",
        "MEASURE",
        "MEASURE_DESCRIPTION",
        "MEASURE_TYPE",
    ]
    with measure_output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=measure_fields, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(measure_catalog)
    return indicator_catalog, measure_catalog, dictionary_files


def load_metric_map(path: Path) -> pd.DataFrame:
    mapping = pd.read_csv(path, dtype=str).fillna("")
    required = {
        "canonical_metric",
        "start_period",
        "end_period",
        "indicator_code",
        "definition_version",
        "rate_kind",
        "comparability_note",
    }
    if set(mapping.columns) != required:
        raise RuntimeError(f"Unexpected metric-map columns in {path}: {list(mapping.columns)}")
    if (~mapping["rate_kind"].isin(["fractional", "count"])).any():
        raise RuntimeError("rate_kind must be fractional or count")
    return mapping


def active_mapping(mapping: pd.DataFrame, period: str) -> pd.DataFrame:
    active = mapping[
        (mapping["start_period"] <= period) & (mapping["end_period"] >= period)
    ].copy()
    if active["canonical_metric"].duplicated().any():
        duplicate = active.loc[
            active["canonical_metric"].duplicated(False), "canonical_metric"
        ].tolist()
        raise RuntimeError(f"Overlapping metric mappings in {period}: {duplicate}")
    if active["indicator_code"].duplicated().any():
        duplicate = active.loc[
            active["indicator_code"].duplicated(False), "indicator_code"
        ].tolist()
        raise RuntimeError(f"One source code maps to multiple metrics in {period}: {duplicate}")
    return active


def materialize_release(release: dict[str, str], release_dir: Path) -> dict[str, str]:
    source_name = urllib.parse.unquote(
        Path(urllib.parse.urlparse(release["data_url"]).path).name
    )
    path = download(release["data_url"], release_dir, f"{release['period']}__{source_name}")
    resolved = dict(release)
    resolved["data_file"] = str(path)
    resolved["data_sha256"] = sha256(path)
    return resolved


def measure_type_lookup(
    measure_catalog: list[dict[str, str]], dictionary_url: str
) -> dict[str, str]:
    return {
        row["MEASURE"]: row["MEASURE_TYPE"]
        for row in measure_catalog
        if row["dictionary_url"] == dictionary_url
    }


def process_release(
    release: dict[str, str],
    mapping: pd.DataFrame,
    measure_catalog: list[dict[str, str]],
    staging_dir: Path,
) -> dict[str, object]:
    active = active_mapping(mapping, release["period"])
    code_records = active.set_index("indicator_code").to_dict(orient="index")
    selected_codes = set(code_records)
    lookup = measure_type_lookup(measure_catalog, release["dictionary_url"])
    zip_path = Path(release["data_file"])
    crc_fallback = False

    def transform(handle: object) -> list[pd.DataFrame]:
        transformed: list[pd.DataFrame] = []
        for chunk in pd.read_csv(
            handle, dtype=str, chunksize=250_000, keep_default_na=False
        ):
            chunk.columns = [column.lstrip("\ufeff") for column in chunk.columns]
            required = {
                "PRACTICE_CODE",
                "PRACTICE_NAME",
                "QUALITY_SERVICE",
                "ACH_DATE",
                "IND_CODE",
                "MEASURE",
                "VALUE",
            }
            if set(chunk.columns) != required:
                raise RuntimeError(
                    f"Unexpected source columns in {zip_path}: {list(chunk.columns)}"
                )
            chunk = chunk[chunk["IND_CODE"].isin(selected_codes)].copy()
            if chunk.empty:
                continue
            for source_code, record in code_records.items():
                mask = chunk["IND_CODE"] == source_code
                for key in [
                    "canonical_metric",
                    "definition_version",
                    "rate_kind",
                    "comparability_note",
                ]:
                    chunk.loc[mask, key] = record[key]
            chunk["release_period"] = release["period"]
            chunk["suppressed"] = chunk["VALUE"].eq("*")
            chunk["value"] = pd.to_numeric(
                chunk["VALUE"].replace({"*": pd.NA, "": pd.NA}), errors="coerce"
            )
            invalid = (
                chunk["value"].isna()
                & ~chunk["suppressed"]
                & chunk["VALUE"].ne("")
            )
            if invalid.any():
                bad = sorted(chunk.loc[invalid, "VALUE"].unique().tolist())
                raise RuntimeError(f"Non-numeric NCDES values in {release['period']}: {bad}")

            chunk["measure_type"] = chunk["MEASURE"].map(
                {
                    "Numerator": "Numerator",
                    "Denominator": "Denominator",
                    "MI Count": "Count",
                    "Management Information": "Count",
                    # Legacy payment files include this supporting extraction count.
                    # It is neither the achievement numerator nor a PCA.
                    "Num Patients in Set": "Supporting",
                }
            )
            missing_type = chunk["measure_type"].isna()
            chunk.loc[missing_type, "measure_type"] = chunk.loc[
                missing_type, "MEASURE"
            ].map(lookup)
            if chunk["measure_type"].isna().any():
                unknown = sorted(
                    chunk.loc[chunk["measure_type"].isna(), "MEASURE"]
                    .unique()
                    .tolist()
                )
                raise RuntimeError(
                    f"Unclassified measures in {release['period']}: {unknown}"
                )
            keep = chunk.rename(
                columns={
                    "PRACTICE_CODE": "gp_code",
                    "PRACTICE_NAME": "practice_name",
                    "QUALITY_SERVICE": "quality_service",
                    "ACH_DATE": "achievement_date",
                    "IND_CODE": "source_indicator_code",
                    "MEASURE": "measure",
                }
            )[
                [
                    "gp_code",
                    "practice_name",
                    "quality_service",
                    "achievement_date",
                    "release_period",
                    "canonical_metric",
                    "source_indicator_code",
                    "definition_version",
                    "rate_kind",
                    "comparability_note",
                    "measure",
                    "measure_type",
                    "value",
                    "suppressed",
                ]
            ]
            transformed.append(keep)
        return transformed

    with zipfile.ZipFile(zip_path) as archive:
        csv_members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(csv_members) != 1:
            raise RuntimeError(f"Expected one CSV in {zip_path}; found {csv_members}")
        csv_member = csv_members[0]
        try:
            with archive.open(csv_member) as handle:
                frames = transform(handle)
        except zipfile.BadZipFile:
            # December 2025 has a central-directory CRC that Python rejects while
            # the system unzip implementation validates and extracts it cleanly.
            crc_fallback = True
            extracted_dir = staging_dir / "_extracted"
            extracted_dir.mkdir(parents=True, exist_ok=True)
            extracted_path = extracted_dir / f"{release['period']}.csv"
            with extracted_path.open("wb") as output_handle:
                completed = subprocess.run(
                    ["unzip", "-p", str(zip_path), csv_member],
                    stdout=output_handle,
                    stderr=subprocess.PIPE,
                    check=False,
                )
            if completed.returncode != 0:
                raise RuntimeError(
                    f"Both Python and system unzip failed for {zip_path}: "
                    f"{completed.stderr.decode('utf-8', errors='replace')}"
                )
            frames = transform(extracted_path)

    if not frames:
        raise RuntimeError(f"No mapped indicators found in {release['period']}")
    result = pd.concat(frames, ignore_index=True)
    found_codes = set(result["source_indicator_code"].unique())
    missing_codes = selected_codes - found_codes
    if missing_codes:
        raise RuntimeError(f"Mapped codes absent from {release['period']}: {sorted(missing_codes)}")
    duplicate_keys = [
        "gp_code",
        "release_period",
        "canonical_metric",
        "measure",
    ]
    duplicates = int(result.duplicated(duplicate_keys).sum())
    if duplicates:
        raise RuntimeError(f"{duplicates} duplicate practice-metric-measure rows in {release['period']}")

    staging_dir.mkdir(parents=True, exist_ok=True)
    output_path = staging_dir / f"ncdes_{release['period']}.parquet"
    result.to_parquet(output_path, index=False, compression="zstd")
    return {
        "period": release["period"],
        "source_rows": len(result),
        "practices": int(result["gp_code"].nunique()),
        "metrics": int(result["canonical_metric"].nunique()),
        "suppressed_values": int(result["suppressed"].sum()),
        "crc_fallback": crc_fallback,
        "staging_file": str(output_path),
        "staging_sha256": sha256(output_path),
    }


def build_panels(
    staging_dir: Path,
    output_dir: Path,
    mapping: pd.DataFrame,
) -> tuple[Path, Path, Path]:
    measure_panel = output_dir / "ncdes_practice_measure_panel.parquet"
    metric_panel = output_dir / "ncdes_practice_metric_panel.parquet"
    wide_panel = output_dir / "ncdes_practice_month.parquet"
    source_glob = str(staging_dir / "ncdes_*.parquet").replace("'", "''")
    connection = duckdb.connect()
    connection.execute(
        f"""
        COPY (
          SELECT * FROM read_parquet('{source_glob}')
          ORDER BY release_period, gp_code, canonical_metric, measure
        ) TO '{measure_panel}' (FORMAT PARQUET, COMPRESSION ZSTD)
        """
    )
    connection.execute(
        f"""
        COPY (
          WITH grouped AS (
            SELECT
              gp_code,
              any_value(practice_name) AS practice_name,
              any_value(quality_service) AS quality_service,
              strftime(strptime(any_value(achievement_date), '%d/%m/%Y'), '%Y-%m') AS month,
              any_value(achievement_date) AS achievement_date,
              release_period,
              canonical_metric,
              any_value(source_indicator_code) AS source_indicator_code,
              any_value(definition_version) AS definition_version,
              any_value(rate_kind) AS rate_kind,
              any_value(comparability_note) AS comparability_note,
              max(value) FILTER (WHERE measure_type = 'Numerator') AS numerator,
              max(value) FILTER (WHERE measure_type = 'Denominator') AS denominator,
              CASE
                WHEN coalesce(bool_or(suppressed) FILTER (WHERE measure_type = 'PCA'), false)
                  THEN NULL
                ELSE coalesce(sum(value) FILTER (WHERE measure_type = 'PCA'), 0)
              END AS pca_total,
              max(value) FILTER (WHERE measure_type = 'Count') AS count,
              coalesce(bool_or(suppressed) FILTER (WHERE measure_type = 'PCA'), false)
                AS pca_suppressed,
              bool_or(suppressed) AS any_suppressed
            FROM read_parquet('{measure_panel}')
            GROUP BY gp_code, release_period, canonical_metric
          )
          SELECT
            *,
            CASE WHEN denominator > 0 THEN 100.0 * numerator / denominator END AS net_rate_pct,
            CASE WHEN denominator + pca_total > 0
              THEN 100.0 * numerator / (denominator + pca_total) END
              AS intervention_coverage_pct,
            CASE WHEN denominator + pca_total > 0
              THEN 100.0 * pca_total / (denominator + pca_total) END AS pca_rate_pct
          FROM grouped
          ORDER BY release_period, gp_code, canonical_metric
        ) TO '{metric_panel}' (FORMAT PARQUET, COMPRESSION ZSTD)
        """
    )

    metrics = sorted(mapping["canonical_metric"].unique().tolist())
    fields = [
        "numerator",
        "denominator",
        "pca_total",
        "count",
        "net_rate_pct",
        "intervention_coverage_pct",
        "pca_rate_pct",
        "pca_suppressed",
        "any_suppressed",
    ]
    expressions = []
    for metric in metrics:
        escaped = metric.replace("'", "''")
        for field in fields:
            aggregate = "bool_or" if field.endswith("suppressed") else "max"
            expressions.append(
                f"{aggregate}({field}) FILTER (WHERE canonical_metric = '{escaped}') "
                f'AS "{metric}_{field}"'
            )
        expressions.append(
            f"any_value(source_indicator_code) FILTER (WHERE canonical_metric = '{escaped}') "
            f'AS "{metric}_source_code"'
        )
        expressions.append(
            f"any_value(definition_version) FILTER (WHERE canonical_metric = '{escaped}') "
            f'AS "{metric}_definition_version"'
        )
    wide_expressions = ",\n              ".join(expressions)
    connection.execute(
        f"""
        COPY (
          SELECT
            gp_code,
            any_value(practice_name) AS practice_name,
            month,
            any_value(achievement_date) AS achievement_date,
            release_period,
            any_value(quality_service) AS quality_service,
            {wide_expressions}
          FROM read_parquet('{metric_panel}')
          GROUP BY gp_code, month, release_period
          ORDER BY month, gp_code
        ) TO '{wide_panel}' (FORMAT PARQUET, COMPRESSION ZSTD)
        """
    )
    connection.close()
    return measure_panel, metric_panel, wide_panel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-period", default="202304", help="YYYYMM, default 202304")
    parser.add_argument("--to-period", default="", help="YYYYMM; default latest found")
    parser.add_argument("--work-dir", type=Path, default=Path("data/ncdes"))
    parser.add_argument("--output-dir", type=Path, default=Path("research/data"))
    parser.add_argument(
        "--metric-map",
        type=Path,
        default=Path("research/pipeline/ncdes_metric_map.csv"),
    )
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument(
        "--reuse-resolved",
        action="store_true",
        help="Reuse publication/resource URLs in the existing source manifest",
    )
    parser.add_argument("--build-panels-only", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.build_panels_only:
        mapping = load_metric_map(args.metric_map)
        paths = build_panels(args.work_dir / "staging", args.output_dir, mapping)
        print(json.dumps({"built_panels": [str(path) for path in paths]}, indent=2))
        return 0

    manifest_path = args.output_dir / "ncdes_source_manifest.json"
    if args.reuse_resolved and manifest_path.exists():
        prior = json.loads(manifest_path.read_text(encoding="utf-8"))
        releases = [
            dict(row)
            for row in prior["releases"]
            if row["period"] >= args.from_period
            and (not args.to_period or row["period"] <= args.to_period)
        ]
    else:
        pages = discover_publication_pages(args.from_period, args.to_period or None)
        if not pages:
            raise RuntimeError("No NCDES publication pages found in requested period")
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            releases = list(executor.map(resolve_publication, pages))
        releases.sort(key=lambda row: row["period"])

    indicator_catalog_path = args.output_dir / "ncdes_indicator_catalog.csv"
    measure_catalog_path = args.output_dir / "ncdes_measure_catalog.csv"
    indicator_catalog, measure_catalog, dictionary_files = build_dictionary_catalogs(
        releases,
        args.work_dir / "dictionaries",
        indicator_catalog_path,
        measure_catalog_path,
    )
    for release in releases:
        dictionary = dictionary_files[release["dictionary_url"]]
        release["dictionary_file"] = dictionary["path"]
        release["dictionary_sha256"] = dictionary["sha256"]

    mapping = load_metric_map(args.metric_map)
    ingestion_summary: dict[str, object] = {}
    if not args.metadata_only:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            releases = list(
                executor.map(
                    lambda release: materialize_release(
                        release, args.work_dir / "releases"
                    ),
                    releases,
                )
            )
        releases.sort(key=lambda row: row["period"])

        staging_dir = args.work_dir / "staging"
        release_checks = []
        for release in releases:
            print(f"processing NCDES {release['period']} ...", flush=True)
            release_checks.append(
                process_release(release, mapping, measure_catalog, staging_dir)
            )
        # Build the multi-million-row panels in a clean process. Repeated pandas
        # chunk parsing can leave enough allocator fragmentation to destabilise
        # the subsequent DuckDB sort in the same process.
        subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--build-panels-only",
                "--work-dir",
                str(args.work_dir),
                "--output-dir",
                str(args.output_dir),
                "--metric-map",
                str(args.metric_map),
            ],
            check=True,
        )
        measure_panel = args.output_dir / "ncdes_practice_measure_panel.parquet"
        metric_panel = args.output_dir / "ncdes_practice_metric_panel.parquet"
        wide_panel = args.output_dir / "ncdes_practice_month.parquet"

        connection = duckdb.connect()
        panel_summary = connection.execute(
            f"""
            SELECT
              count(*) AS metric_rows,
              count(DISTINCT gp_code) AS distinct_practices,
              count(DISTINCT month) AS distinct_months,
              min(month) AS first_month,
              max(month) AS last_month,
              count(DISTINCT canonical_metric) AS distinct_metrics,
              sum(CASE WHEN any_suppressed THEN 1 ELSE 0 END) AS rows_with_suppression,
              sum(CASE WHEN rate_kind = 'fractional' AND numerator IS NULL
                        AND NOT any_suppressed THEN 1 ELSE 0 END)
                AS unexplained_missing_numerators,
              sum(CASE WHEN rate_kind = 'fractional' AND denominator IS NULL
                        AND NOT any_suppressed THEN 1 ELSE 0 END)
                AS unexplained_missing_denominators,
              sum(CASE WHEN rate_kind = 'count' AND count IS NULL
                        AND NOT any_suppressed THEN 1 ELSE 0 END)
                AS unexplained_missing_counts,
              sum(CASE WHEN numerator > denominator THEN 1 ELSE 0 END)
                AS numerators_over_denominators
            FROM read_parquet('{metric_panel}')
            """
        ).fetchdf().iloc[0].to_dict()
        negative_values = connection.execute(
            f"SELECT count(*) FROM read_parquet('{measure_panel}') WHERE value < 0"
        ).fetchone()[0]
        wide_rows = connection.execute(
            f"SELECT count(*) FROM read_parquet('{wide_panel}')"
        ).fetchone()[0]
        connection.close()
        panel_summary = {
            key: (value.item() if hasattr(value, "item") else value)
            for key, value in panel_summary.items()
        }
        panel_summary["negative_source_values"] = int(negative_values)
        panel_summary["wide_practice_month_rows"] = int(wide_rows)
        failures = {
            key: panel_summary[key]
            for key in [
                "unexplained_missing_numerators",
                "unexplained_missing_denominators",
                "unexplained_missing_counts",
                "numerators_over_denominators",
                "negative_source_values",
            ]
            if panel_summary[key]
        }
        if failures:
            raise RuntimeError(f"NCDES validation failures: {failures}")

        ingestion_summary = {
            "release_checks": release_checks,
            "panel_summary": panel_summary,
            "outputs": {
                "measure_panel": {
                    "path": str(measure_panel),
                    "sha256": sha256(measure_panel),
                },
                "metric_panel": {
                    "path": str(metric_panel),
                    "sha256": sha256(metric_panel),
                },
                "wide_panel": {
                    "path": str(wide_panel),
                    "sha256": sha256(wide_panel),
                },
            },
        }
        validation_path = args.output_dir / "ncdes_ingestion_validation.json"
        validation_path.write_text(
            json.dumps(ingestion_summary, indent=2, default=str) + "\n",
            encoding="utf-8",
        )

    manifest = {
        "series_url": SERIES_URL,
        "retrieved_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "from_period": releases[0]["period"],
        "to_period": releases[-1]["period"],
        "release_count": len(releases),
        "indicator_catalog_rows": len(indicator_catalog),
        "measure_catalog_rows": len(measure_catalog),
        "metric_map": str(args.metric_map),
        "metric_map_sha256": sha256(args.metric_map),
        "releases": releases,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "release_count": len(releases),
                "from_period": releases[0]["period"],
                "to_period": releases[-1]["period"],
                "distinct_dictionaries": len({row["dictionary_url"] for row in releases}),
                "indicator_catalog_rows": len(indicator_catalog),
                "measure_catalog_rows": len(measure_catalog),
                "manifest": str(manifest_path),
                "indicator_catalog": str(indicator_catalog_path),
                "measure_catalog": str(measure_catalog_path),
                "metadata_only": args.metadata_only,
                "ingestion": ingestion_summary.get("panel_summary", {}),
            },
            indent=2,
            default=str,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
