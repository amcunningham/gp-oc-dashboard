"""Validation gates — the safety catch before anything is published.

The pipeline must never ship silently-broken data to a public tool that names practices.
Your own PANEL_NOTES catalogue the failures an unattended run would otherwise push live:
the corrupt panel CSV that dropped 96 practices, the workforce x2 doubling, sentinel codes,
component-vs-total inconsistencies. Each gate below turns one of those into an automatic stop.

Each gate returns (name, passed: bool, detail: str). refresh.py fails the whole run — so no
Pull Request is opened — if ANY gate fails.
"""
import duckdb


def gate(name, passed, detail=""):
    return (name, bool(passed), str(detail))


def validate_gpad_release(agg_csv, months_expected=3, practices_min=5800, practices_max=6600):
    """Structural gates on a freshly aggregated GPAD per-release file (from agg_duck2.py)."""
    con = duckdb.connect()
    df = con.execute(f"SELECT * FROM read_csv_auto('{agg_csv}')").df()
    results = []

    # 1. Non-empty.
    results.append(gate("rows_present", len(df) > 0, f"{len(df)} practice-months"))

    # 2. GPAD ships exactly 3 months per release — fewer means a truncated/corrupt download.
    nmonths = df["month"].nunique()
    results.append(gate("months_in_release", nmonths == months_expected,
                        f"{nmonths} distinct months (expected {months_expected}): "
                        f"{sorted(df['month'].unique().tolist())}"))

    # 3. Practice count per month within a sane band — catches the '96 dropped practices' class.
    per = df.groupby("month")["gp_code"].nunique()
    ok = bool(per.between(practices_min, practices_max).all())
    results.append(gate("practice_count_band", ok,
                        f"per-month distinct practices {per.to_dict()} "
                        f"(band {practices_min}-{practices_max})"))

    # 4. No negative counts (sentinel values / parse corruption leaking through).
    count_cols = [c for c in df.columns if c not in ("month", "gp_code")]
    negs = int((df[count_cols] < 0).sum().sum())
    results.append(gate("no_negative_counts", negs == 0, f"{negs} negative cells"))

    # 5. Component sanity: no sub-count may exceed the row total.
    comps = [c for c in ["same_day", "next_day", "gp", "f2f", "phone", "online", "dna", "attended"]
             if c in df.columns]
    bad = int(sum((df[c] > df["total"]).sum() for c in comps))
    results.append(gate("components_le_total", bad == 0, f"{bad} rows with a component > total"))

    return results


# When the pipeline is extended to rebuild the cross-section, add gates that reproduce your
# documented reconciliations before publishing, e.g.:
#   - national GPPS headline reproduces the published figure to ~0.05pp (base-weighted)
#   - workforce FTE is NOT 2x the workforce_panel (the x2 bug guard)
#   - xsec practice count does not fall vs the previous build (no silent drop)
