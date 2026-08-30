#!/usr/bin/env python3
"""Reconcile the latest raw NCDES extract with the processed metric panel."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import duckdb
import pandas as pd


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest", type=Path, default=Path("research/data/ncdes_source_manifest.json")
    )
    parser.add_argument(
        "--metric-map", type=Path, default=Path("research/pipeline/ncdes_metric_map.csv")
    )
    parser.add_argument(
        "--metric-panel",
        type=Path,
        default=Path("research/data/ncdes_practice_metric_panel.parquet"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("research/data/ncdes_latest_reconciliation.json"),
    )
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    latest = manifest["releases"][-1]
    period = latest["period"]
    raw_path = Path(latest["data_file"])
    if sha256(raw_path) != latest["data_sha256"]:
        raise RuntimeError("Latest raw ZIP hash does not match the source manifest")

    mapping = pd.read_csv(args.metric_map, dtype=str)
    active = mapping[
        (mapping["start_period"] <= period) & (mapping["end_period"] >= period)
    ].copy()
    code_to_metric = active.set_index("indicator_code")["canonical_metric"].to_dict()

    with zipfile.ZipFile(raw_path) as archive:
        members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(members) != 1:
            raise RuntimeError(f"Expected one CSV in {raw_path}; found {members}")
        with archive.open(members[0]) as handle:
            raw = pd.read_csv(handle, dtype=str, keep_default_na=False)
    raw = raw[raw["IND_CODE"].isin(code_to_metric)].copy()
    raw["value_numeric"] = pd.to_numeric(
        raw["VALUE"].replace({"*": pd.NA, "": pd.NA}), errors="coerce"
    )

    connection = duckdb.connect()
    processed = connection.execute(
        """
        SELECT
          canonical_metric,
          any_value(source_indicator_code) AS source_indicator_code,
          count(DISTINCT gp_code) AS practices,
          sum(numerator) AS numerator,
          sum(denominator) AS denominator,
          sum(count) AS count_value
        FROM read_parquet(?)
        WHERE release_period = ?
        GROUP BY canonical_metric
        """,
        [str(args.metric_panel), period],
    ).fetchdf()
    connection.close()
    processed = processed.set_index("canonical_metric")

    comparisons = []
    for source_code, metric in sorted(code_to_metric.items(), key=lambda item: item[1]):
        rows = raw[raw["IND_CODE"] == source_code]

        def source_sum(labels: set[str]) -> float | None:
            values = rows.loc[rows["MEASURE"].isin(labels), "value_numeric"]
            result = values.sum(min_count=1)
            return None if pd.isna(result) else float(result)

        raw_values = {
            "practices": int(rows["PRACTICE_CODE"].nunique()),
            "numerator": source_sum({"Numerator"}),
            "denominator": source_sum({"Denominator"}),
            "count_value": source_sum({"MI Count", "Management Information"}),
        }
        panel_row = processed.loc[metric]
        panel_values = {
            "practices": int(panel_row["practices"]),
            "numerator": None
            if pd.isna(panel_row["numerator"])
            else float(panel_row["numerator"]),
            "denominator": None
            if pd.isna(panel_row["denominator"])
            else float(panel_row["denominator"]),
            "count_value": None
            if pd.isna(panel_row["count_value"])
            else float(panel_row["count_value"]),
        }
        matches = raw_values == panel_values and panel_row["source_indicator_code"] == source_code
        comparisons.append(
            {
                "canonical_metric": metric,
                "source_indicator_code": source_code,
                "raw": raw_values,
                "processed": panel_values,
                "matches": bool(matches),
            }
        )

    output = {
        "period": period,
        "raw_file": str(raw_path),
        "raw_sha256": sha256(raw_path),
        "metric_panel": str(args.metric_panel),
        "metric_panel_sha256": sha256(args.metric_panel),
        "comparison_count": len(comparisons),
        "all_match": all(row["matches"] for row in comparisons),
        "comparisons": comparisons,
    }
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    return 0 if output["all_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
