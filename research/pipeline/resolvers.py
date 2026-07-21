"""Release resolvers: discover the latest available edition of each open NHS data source.

The hard, source-facing part of the pipeline. NHS England / NHS Digital publish at opaque,
NON-templatable URLs (e.g.
  https://files.digital.nhs.uk/BC/A65BD0/Practice_Level_Crosstab_Feb_26.zip),
so we can't construct next month's URL — we read the publication page and extract it. For GPAD
the download zips live on per-edition sub-pages (…/appointments-in-general-practice/may-2026),
not the landing page, so we follow the newest editions and scan those.

Each resolver returns {"period": "YYYYMM", "label": "Mon_YY", "url": "..."} for the newest
edition found, or None. Every resolver honours a manual override env var (GPAD_OVERRIDE_URL).
"""
import calendar
import os
import re
import requests

# Browser-like User-Agent: NHS Digital / gov sites frequently 403 a bare python-requests UA,
# especially from a CI datacentre IP. This makes the request look like an ordinary browser.
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

MONTHS = {m: f"{i:02d}" for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}
NUM_TO_MON = {v: k for k, v in MONTHS.items()}
MONTH_IX = {name.lower(): i for i, name in enumerate(calendar.month_name) if name}  # january -> 1

# Full https URL incl. the opaque hash path (non-greedy), so we match the real download link.
CROSSTAB_RE = re.compile(
    r"https://files\.digital\.nhs\.uk/\S+?/Practice_Level_Crosstab_([A-Z][a-z]{2})_(\d{2})\.zip")
# Per-edition sub-page slugs like 'may-2026'.
EDITION_RE = re.compile(
    r"/data-and-information/publications/statistical/appointments-in-general-practice/([a-z]+-\d{4})")
EDITION_BASE = "https://digital.nhs.uk/data-and-information/publications/statistical/appointments-in-general-practice/"


def _get(url, timeout=60):
    r = requests.get(url, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.text


def _period(mon, yy):
    return f"20{yy}{MONTHS[mon]}"


def resolve_gpad(publication_url):
    """Latest 'Appointments in General Practice' practice-level crosstab release."""
    override = os.environ.get("GPAD_OVERRIDE_URL")
    if override:
        m = CROSSTAB_RE.search(override)
        if not m:
            raise ValueError("GPAD_OVERRIDE_URL is set but is not a crosstab .zip URL")
        return {"period": _period(*m.groups()), "label": f"{m.group(1)}_{m.group(2)}", "url": override}

    found = {}  # period -> url
    landing = _get(publication_url)
    for m in CROSSTAB_RE.finditer(landing):
        found[_period(*m.groups())] = m.group(0)

    # Zips normally sit on per-edition sub-pages. Visit the newest editions BY REAL DATE
    # (not alphabetically) and scan each for the crosstab download.
    if not found:
        def slug_date(slug):
            mon, yr = slug.split("-")
            return (int(yr), MONTH_IX.get(mon, 0))

        for slug in sorted(set(EDITION_RE.findall(landing)), key=slug_date, reverse=True)[:3]:
            try:
                page = _get(EDITION_BASE + slug)
            except requests.RequestException:
                continue
            for m in CROSSTAB_RE.finditer(page):
                found[_period(*m.groups())] = m.group(0)

    if not found:
        return None

    period = max(found)
    return {"period": period, "label": f"{NUM_TO_MON[period[4:6]]}_{period[2:4]}", "url": found[period]}


# To add a source later, write resolve_<name>(publication_url) with the same return shape and a
# <NAME>_OVERRIDE_URL fallback. CBT / OC / workforce / FFT all follow this pattern.
