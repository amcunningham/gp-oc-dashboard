#!/usr/bin/env python3
"""Phase-1 auto-refresh pipeline (single source: GPAD) with a human PR-review gate.

Flow:
  resolve latest edition  ->  compare to data_manifest.json  ->  if new:
    download zip  ->  aggregate (reusing research/scripts/agg_duck2.py)  ->  validation gates
    ->  update manifest + write the PR body.
The GitHub Actions workflow then opens a Pull Request; merging it triggers the Pages deploy.

Exit codes:
  0  success (whether or not there was new data)
  1  a validation gate FAILED  -> the run goes red, no PR is opened
  2  a structural problem (e.g. no crosstab in the zip) that needs a human to look

Outputs written to $GITHUB_OUTPUT (consumed by the workflow): changed, period, label.
"""
import argparse
import datetime
import glob
import json
import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

import resolvers
import validate

PIPE = Path(__file__).resolve().parent               # research/pipeline
ROOT = PIPE.parents[1]                               # repo root
MANIFEST = PIPE / "data_manifest.json"
AGG_SCRIPT = ROOT / "research" / "scripts" / "agg_duck2.py"
AGG_OUT_DIR = ROOT / "research" / "data" / "gpad_agg"
WORK = PIPE / "_work"                                 # gitignored scratch


def out(key, val):
    gh = os.environ.get("GITHUB_OUTPUT")
    if gh:
        with open(gh, "a") as f:
            f.write(f"{key}={val}\n")
    print(f"::output:: {key}={val}")


def write_pr_body(text):
    (PIPE / "_pr_body.md").write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="gpad")
    args = ap.parse_args()
    if args.source != "gpad":
        print("Phase 1 wires GPAD only. Add sources as resolvers.resolve_<name>.", file=sys.stderr)
        return 2

    man = json.loads(MANIFEST.read_text())
    src = man["sources"]["gpad"]
    src["last_checked_utc"] = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

    latest = resolvers.resolve_gpad(src["publication_url"])
    if latest is None:
        print("Resolver found no release — the page structure may have changed. VERIFY.")
        MANIFEST.write_text(json.dumps(man, indent=2) + "\n")
        out("changed", "false")
        return 0

    print(f"latest available: {latest['label']} ({latest['period']})  |  manifest: {src['latest_period']}")
    if latest["period"] <= str(src["latest_period"]):
        print("Nothing new.")
        MANIFEST.write_text(json.dumps(man, indent=2) + "\n")
        out("changed", "false")
        return 0

    # --- new edition: download + unzip ---
    WORK.mkdir(exist_ok=True)
    AGG_OUT_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = WORK / f"{latest['label']}.zip"
    print("downloading", latest["url"])
    urllib.request.urlretrieve(latest["url"], zip_path)          # NHS files are plain https
    ex = WORK / latest["label"]
    ex.mkdir(exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(ex)
    if not glob.glob(str(ex / "Practice_Level_Crosstab*.csv")):
        print("No Practice_Level_Crosstab*.csv found in the zip — VERIFY archive layout.", file=sys.stderr)
        return 2

    # --- aggregate using the repo's OWN script (single source of truth for the schema) ---
    agg_out = AGG_OUT_DIR / f"gpad_{latest['label']}.csv"
    subprocess.run(
        [sys.executable, str(AGG_SCRIPT), str(agg_out), str(ex / "Practice_Level_Crosstab*.csv")],
        check=True)

    # --- validation gates ---
    gates = validate.validate_gpad_release(
        str(agg_out),
        practices_min=src["expected_practices_min"],
        practices_max=src["expected_practices_max"])
    report = "\n".join(f"- {'✅' if p else '❌'} **{n}** — {d}" for n, p, d in gates)
    print(report)
    if any(not p for _, p, _ in gates):
        write_pr_body("### Validation FAILED — not published\n\n" + report)
        print("\nOne or more gates FAILED — refusing to publish.", file=sys.stderr)
        return 1

    # --- passed: update manifest ---
    src["latest_period"] = latest["period"]
    src["latest_release_label"] = latest["label"]
    src["last_resolved_url"] = latest["url"]
    MANIFEST.write_text(json.dumps(man, indent=2) + "\n")

    # --- INTEGRATION HOOK (phase 1 stops here) ---------------------------------------------
    # To make the *live pages* update, this release's 3 months must be merged into
    # panel_merged and the cross-section rebuilt. Wire your existing assembly here once you're
    # ready, e.g.:
    #   subprocess.run([sys.executable, str(ROOT / "research" / "scripts" / "build_xsec_full.py")], check=True)
    # and add the cross-section gates noted at the bottom of validate.py. Until then the PR
    # carries the new per-release aggregate + the manifest bump, which is the spine working
    # end to end and safe to merge.
    # ---------------------------------------------------------------------------------------

    body = (
        f"## Automated data refresh — GPAD {latest['label']} ({latest['period']})\n\n"
        f"- **Source:** {src['publication_url']}\n"
        f"- **Resolved file:** {latest['url']}\n"
        f"- **New aggregate:** `research/data/gpad_agg/gpad_{latest['label']}.csv`\n\n"
        f"### Validation gates\n{report}\n\n"
        f"Review the figures, then **merge to publish** (merge triggers the Pages deploy).\n\n"
        f"_Generated by `research/pipeline/refresh.py`. Phase 1 = detect + aggregate + gate + PR; "
        f"the panel/cross-section rebuild hook is marked in that file._")
    write_pr_body(body)
    out("changed", "true")
    out("period", latest["period"])
    out("label", latest["label"])
    print("OK — ready for PR")
    return 0


if __name__ == "__main__":
    sys.exit(main())
