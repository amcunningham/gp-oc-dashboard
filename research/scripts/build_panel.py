#!/usr/bin/env python3
"""
Build a practice x date (x hour) panel of contact demand across many months.

Run on a machine with network access:

    python build_panel.py --from 2025-01 --to 2026-06 --out research/data/panel

For each month it finds the publication page, downloads the three files below, reduces each to a
compact table, writes a parquet, and deletes the raw download. Peak disk use is one month's raw
files; the output is a few megabytes a month.

    Cloud Based Telephony, By Day and Time   -> practice x date x time band: inbound, IVR-ended, answered
    Cloud Based Telephony, By Durations      -> practice x date: total inbound, total answered (a check)
    OC Submissions, By Day and Time          -> practice x date x hour band: total, clinical, admin

Coverage. Monthly telephony editions exist from October 2025 only; earlier months appear as
aggregates inside later publications, not as daily files. Online consultation day and time exists
earlier, but the editions up to at least October 2025 are aggregated to weekday rather than dated —
the file size gives it away, about 1 MB when aggregated and about 11 MB when dated. The script
reports which is which as it goes.

    --skip-oc / --skip-cbt   fetch one collection only
    --keep-raw               do not delete the downloaded zips
    --resume                 skip months whose parquet already exists (default on)
"""
import argparse, io, os, re, sys, time, zipfile
from pathlib import Path

import pandas as pd

try:
    import requests
except ImportError:
    sys.exit("pip install requests pandas pyarrow")

MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
CBT_PAGE = ("https://digital.nhs.uk/data-and-information/publications/statistical/"
            "cloud-based-telephony-data-in-general-practice/{slug}")
OC_PAGE = ("https://digital.nhs.uk/data-and-information/publications/statistical/"
           "submissions-via-online-consultation-systems-in-general-practice/{slug}")
LINK = re.compile(r'https://files\.digital\.nhs\.uk/[A-Z0-9]{2}/[A-Z0-9]+/[^"\'<>\s]+\.zip')


def months_between(a, b):
    y, m = map(int, a.split("-")); Y, M = map(int, b.split("-"))
    while (y, m) <= (Y, M):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def say(*a):
    print(*a, flush=True)


def find_link(session, page_url, needle):
    try:
        r = session.get(page_url, timeout=60); r.raise_for_status()
    except Exception as e:
        return None, f"page failed: {e}"
    from urllib.parse import unquote
    for u in sorted(set(LINK.findall(r.text))):
        if needle.lower() in unquote(u).lower():
            return u, None
    return None, f"no link matching '{needle}'"


def fetch_zip(session, url, label=""):
    with session.get(url, stream=True, timeout=900) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        buf = io.BytesIO(); done = 0; last = 0
        for chunk in r.iter_content(1 << 20):
            buf.write(chunk); done += len(chunk)
            if done - last >= 10 << 20:
                last = done
                pct = f" ({done/total:.0%})" if total else ""
                print(f"\r      {label} downloading {done/1e6:6.0f} MB{pct}", end="", flush=True)
        print(f"\r      {label} downloaded  {done/1e6:6.0f} MB          ", flush=True)
    buf.seek(0)
    return zipfile.ZipFile(buf)


def csvs(z):
    for n in z.namelist():
        if n.lower().endswith(".csv") and "unmapped" not in n.lower():
            with z.open(n) as h:
                yield n, io.BytesIO(h.read())


def reduce_cbt_daytime(z):
    out = []
    for _, fh in csvs(z):
        d = pd.read_csv(fh, low_memory=False)
        d.columns = [c.strip() for c in d.columns]
        need = {"Date", "PRACTICE_CODE", "Indicator", "Value"}
        if not need.issubset(d.columns):
            continue
        tcol = next((c for c in d.columns if "time" in c.lower() and "date" not in c.lower()), None)
        if tcol is None:
            continue
        d = d[["Date", "PRACTICE_CODE", "PCN_CODE", "SUB_ICB_LOCATION_CODE", "Indicator", tcol, "Value"]]
        d = d.rename(columns={"Date": "date", "PRACTICE_CODE": "gp_code", tcol: "band"})
        out.append(d)
    if not out:
        return None
    d = pd.concat(out, ignore_index=True)
    d["date"] = pd.to_datetime(d["date"], errors="coerce")
    w = d.pivot_table(index=["gp_code", "PCN_CODE", "SUB_ICB_LOCATION_CODE", "date", "band"],
                      columns="Indicator", values="Value", aggfunc="sum").reset_index()
    w.columns.name = None
    ren = {"CBT001": "inbound", "CBT002": "ivr_ended", "CBT003": "answered"}
    return w.rename(columns={k: v for k, v in ren.items() if k in w.columns})


def reduce_cbt_durations(z):
    out = []
    for _, fh in csvs(z):
        d = pd.read_csv(fh, usecols=lambda c: c.strip() in
                        {"Date", "PRACTICE_CODE", "Indicator", "Duration", "Value"}, low_memory=False)
        d.columns = [c.strip() for c in d.columns]
        out.append(d[d.Indicator.isin(["CBT001", "CBT003"])])
    if not out:
        return None
    d = pd.concat(out, ignore_index=True).rename(columns={"PRACTICE_CODE": "gp_code", "Date": "date"})
    d["date"] = pd.to_datetime(d["date"], errors="coerce")
    inb = (d[(d.Indicator == "CBT001") & (d.Duration == "TOTAL")]
           .groupby(["gp_code", "date"], as_index=False).Value.sum().rename(columns={"Value": "inbound_total"}))
    ans = (d[d.Indicator == "CBT003"]
           .groupby(["gp_code", "date"], as_index=False).Value.sum().rename(columns={"Value": "answered_total"}))
    return inb.merge(ans, on=["gp_code", "date"], how="outer")


def reduce_oc(z):
    out = []
    for _, fh in csvs(z):
        d = pd.read_csv(fh, low_memory=False)
        d.columns = [c.strip() for c in d.columns]
        if "DATE" not in d.columns or "GP_CODE" not in d.columns:
            continue
        keep = [c for c in ["DATE", "GP_CODE", "PCN_CODE", "SUB_ICB_LOCATION_CODE",
                            "SUBMISSION_TIME", "CLINICAL", "ADMIN", "UNKNOWN_OTHER", "TOTAL"]
                if c in d.columns]
        out.append(d[keep])
    if not out:
        return "no DATE column: this edition is aggregated to weekday, not dated"
    d = pd.concat(out, ignore_index=True).rename(columns={"DATE": "date", "GP_CODE": "gp_code",
                                                          "SUBMISSION_TIME": "band"})
    d["date"] = pd.to_datetime(d["date"], errors="coerce")
    grp = [c for c in ["gp_code", "PCN_CODE", "SUB_ICB_LOCATION_CODE", "date", "band"] if c in d.columns]
    vals = [c for c in ["CLINICAL", "ADMIN", "UNKNOWN_OTHER", "TOTAL"] if c in d.columns]
    return d.groupby(grp, as_index=False)[vals].sum()


JOBS = [
    ("cbt_daytime", CBT_PAGE, "By Day and Time", reduce_cbt_daytime),
    ("cbt_durations", CBT_PAGE, "By Durations", reduce_cbt_durations),
    ("oc_daytime", OC_PAGE, "By Day and Time", reduce_oc),
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from", dest="frm", default="2025-10")
    p.add_argument("--to", dest="to", default="2026-06")
    p.add_argument("--out", default="panel")
    p.add_argument("--skip-oc", action="store_true")
    p.add_argument("--skip-cbt", action="store_true")
    p.add_argument("--keep-raw", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="list the URLs it would fetch and stop")
    a = p.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    s = requests.Session(); s.headers["User-Agent"] = "gp-panel-build/1.0"
    n_months = len(list(months_between(a.frm, a.to)))
    say(f"{n_months} months, {a.frm} to {a.to} -> {out.resolve()}")
    say("each month fetches up to three files; large ones take a few minutes each\n")

    for y, m in months_between(a.frm, a.to):
        slug = f"{MONTHS[m-1]}-{y}"; tag = f"{y}-{m:02d}"
        for key, page, needle, reducer in JOBS:
            if a.skip_oc and key.startswith("oc"):
                continue
            if a.skip_cbt and key.startswith("cbt"):
                continue
            dest = out / f"{key}_{tag}.parquet"
            if dest.exists():
                say(f"{tag} {key:14s} already built, skipping"); continue
            say(f"{tag} {key:14s} looking up {slug} ...")
            url, err = find_link(s, page.format(slug=slug), needle)
            if not url:
                say(f"{tag} {key:14s} {err}"); continue
            if a.dry_run:
                say(f"{tag} {key:14s} would fetch {url}"); continue
            try:
                z = fetch_zip(s, url, label=key)
                say(f"      {key} reducing ...")
                df = reducer(z)
            except Exception as e:
                say(f"{tag} {key:14s} failed: {e}"); continue
            if isinstance(df, str):
                say(f"{tag} {key:14s} {df}"); continue
            if df is None or not len(df):
                say(f"{tag} {key:14s} produced nothing"); continue
            df["month"] = tag
            df.to_parquet(dest, index=False)
            say(f"{tag} {key:14s} {len(df):>9,} rows  {dest.stat().st_size/1e6:6.1f} MB  "
                f"{df.gp_code.nunique():,} practices")
            time.sleep(1)

    say(f"\nwritten to {out.resolve()}")
    for key in ["cbt_daytime", "cbt_durations", "oc_daytime"]:
        f = sorted(out.glob(f"{key}_*.parquet"))
        if f:
            mb = sum(x.stat().st_size for x in f) / 1e6
            say(f"  {key:14s} {len(f)} months, {mb:.0f} MB")


if __name__ == "__main__":
    main()
