"""
POA&M generation.

A Plan of Action and Milestones (POA&M) is the standard artifact for tracking
unmet controls: what is deficient, how it will be fixed, and by when. Every
failed or manual-review control becomes a row here. This is the kind of document
a GovCon compliance analyst produces constantly, so generating it automatically
from the assessment results is the whole point.
"""

import csv
from datetime import date, timedelta


# Default remediation windows by control weight. Heavier controls get a tighter
# deadline because their gaps are higher risk.
_DAYS_BY_WEIGHT = {5: 30, 3: 60, 1: 90}


def build_poam_rows(results, start=None):
    """Turn failed and manual controls into POA&M rows with target dates."""
    start = start or date.today()
    rows = []
    open_items = [r for r in results if r["status"] in ("fail", "manual")]
    # Sort so the highest-weight gaps sit at the top of the plan.
    open_items.sort(key=lambda r: (-r["weight"], r["id"]))

    for i, item in enumerate(open_items, start=1):
        due = start + timedelta(days=_DAYS_BY_WEIGHT.get(item["weight"], 90))
        finding = (
            "Requires manual validation."
            if item["status"] == "manual"
            else "Control not met per automated assessment."
        )
        rows.append({
            "item": "POAM-%03d" % i,
            "control_id": item["id"],
            "family": item["family"],
            "weakness": "%s: %s" % (item["title"], finding),
            "weight": item["weight"],
            "planned_remediation": item["remediation"] or "Define and implement corrective action.",
            "target_date": due.isoformat(),
            "status": "Open",
        })
    return rows


def write_csv(rows, path):
    """Write POA&M rows to a CSV that opens cleanly in Excel."""
    fields = ["item", "control_id", "family", "weakness", "weight",
              "planned_remediation", "target_date", "status"]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
