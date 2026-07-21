"""Release resolvers: discover the latest available edition of each open NHS data source.

This is the hard, source-facing part of the auto-refresh pipeline. NHS England / NHS Digital
publish at opaque, NON-templatable URLs (e.g.
  https://files.digital.nhs.uk/BC/A65BD0/Practice_Level_Crosstab_Feb_26.zip),
so we cannot construct next month's URL — we have to read the publication page and extract it.

Each resolver returns {"period": "YYYYMM", "label": "Mon_YY", "url": "..."} for the newest
edition it can find, or None. `period` is a string that sorts correctly as YYYYMM.

VERIFY the scraping against the live page before trusting unattended runs — page structure
changes. Every resolver honours a manual override env var as a fallback (e.g. GPAD_OVERRIDE_URL),
so the pipeline stays usable even if a selector breaks.
"""
import os
import re
import requests

UA = {"User-Agent": "gp-oc-dashboard data-refresh (+https://github.com/amcunningham/gp-oc-dashboard)"}

MONTHS = {m: f"{i:02d}" for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}
NUM_TO_MON = {v: k for k, v in MONTHS.items()}

# Full https URL incl. the opaque two hash segments, so we match the real download link.
CROSSTAB_RE = re.compile(
    r"https://files\.digital\.nhs\.uk/[0-9A-Fa-f]{2}/[0-9A-Fa-f]{6}/"
    r"Practice_Level_Crosstab_([A-Z][a-z]{2})_(\d{2})\.zip")


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

    def scan(html):
        for m in CROSSTAB_RE.finditer(html):
            found[_period(*m.groups())] = m.group(0)

    scan(_get(publication_url))

    # Fallback: the landing page may only link to per-edition sub-pages rather than the zip
    # directly. Follow the most recent-looking edition links and scan those.
    # VERIFY this href pattern against the live page if the direct scan ever returns nothing.
    if not found:
        edition_paths = sorted(set(re.findall(
            r'href="(/data-and-information/publications/statistical/'
            r'appointments-in-general-practice/[a-z0-9-]+)"', _get(publication_url))))
        for path in edition_paths[-4:]:          # newest few editions
            try:
                scan(_get("https://digital.nhs.uk" + path))
            except requests.RequestException:
                continue

    if not found:
        return None

    period = max(found)
    label = f"{NUM_TO_MON[period[4:6]]}_{period[2:4]}"
    return {"period": period, "label": label, "url": found[period]}


# --- To add a source later, write resolve_<name>(publication_url) returning the same dict. ---
# The pattern is identical: GET the publication page, regex the real file URL, parse period,
# support a <NAME>_OVERRIDE_URL fallback. CBT / OC / workforce / FFT all follow this shape.
