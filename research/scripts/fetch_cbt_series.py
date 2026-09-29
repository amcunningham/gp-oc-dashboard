#!/usr/bin/env python3
"""
Fetch the Cloud Based Telephony practice-level daily files for a range of months.

Run this on a machine with network access (not in the Cowork sandbox):

    python fetch_cbt_series.py --from 2025-07 --to 2026-06 --out research/data/cbt_series

Each monthly publication page carries hashed file URLs, so the links have to be read
off the page rather than constructed. This fetches the page, picks the zips we need,
and skips anything already downloaded.

Files fetched per month:
  - "Cloud Based Telephony By Durations"        CBT001 total inbound, CBT003 answered, by date
  - "Cloud Based Telephony Calls Answered"      answered by date, wait-time band, core window
  - "Cloud Based Telephony By Day and Time"     by date and hour band   (--daytime)
"""
import argparse, re, sys, time
from pathlib import Path
from urllib.parse import unquote

try:
    import requests
except ImportError:
    sys.exit("pip install requests")

BASE = ("https://digital.nhs.uk/data-and-information/publications/statistical/"
        "cloud-based-telephony-data-in-general-practice/{slug}")
MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
WANT = {"durations": "By Durations", "answered": "Calls Answered Metric"}
DAYTIME = {"daytime": "By Day and Time"}
LINK = re.compile(r'https://files\.digital\.nhs\.uk/[A-Z0-9]{2}/[A-Z0-9]+/[^"\'<>\s]+\.zip')


def months_between(a, b):
    y, m = map(int, a.split("-"))
    Y, M = map(int, b.split("-"))
    while (y, m) <= (Y, M):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from", dest="frm", default="2025-07", help="first month, YYYY-MM (series starts 2025-01)")
    p.add_argument("--to", dest="to", default="2026-06", help="last month, YYYY-MM")
    p.add_argument("--out", default="cbt_series", help="output directory")
    p.add_argument("--daytime", action="store_true", help="also fetch the By Day and Time zip (hour bands)")
    a = p.parse_args()

    want = dict(WANT)
    if a.daytime:
        want.update(DAYTIME)

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = "cbt-series-fetch/1.0"

    for y, m in months_between(a.frm, a.to):
        slug = f"{MONTHS[m - 1]}-{y}"
        tag = f"{y}-{m:02d}"
        try:
            r = s.get(BASE.format(slug=slug), timeout=60)
            r.raise_for_status()
        except Exception as e:
            print(f"{tag}  page failed: {e}")
            continue

        links = sorted(set(LINK.findall(r.text)))
        got = 0
        for key, needle in want.items():
            hit = next((u for u in links if needle.lower() in unquote(u).lower()), None)
            if not hit:
                print(f"{tag}  no '{needle}' zip on page")
                continue
            dest = out / f"cbt_{key}_{tag}.zip"
            if dest.exists() and dest.stat().st_size > 0:
                got += 1
                continue
            try:
                with s.get(hit, stream=True, timeout=600) as d:
                    d.raise_for_status()
                    tmp = dest.with_suffix(".part")
                    with open(tmp, "wb") as f:
                        for chunk in d.iter_content(1 << 20):
                            f.write(chunk)
                    tmp.rename(dest)
                got += 1
                print(f"{tag}  {key:9s} {dest.stat().st_size / 1e6:6.1f} MB")
            except Exception as e:
                print(f"{tag}  {key} download failed: {e}")
        if got:
            print(f"{tag}  ok ({got}/{len(want)})")
        time.sleep(1)

    print(f"\ndone -> {out.resolve()}")


if __name__ == "__main__":
    main()
