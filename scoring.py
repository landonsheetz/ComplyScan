"""
SPRS-style scoring.

DoD's Supplier Performance Risk System (SPRS) methodology for NIST SP 800-171
starts every assessment at 110 (one point per control) and subtracts a weighted
value for each control that is NOT met:

    weight 5   controls whose absence exposes the network broadly
    weight 3   controls with a significant but narrower impact
    weight 1   everything else

A perfect score is 110. The score can go negative, because some weight-5 gaps
cost more than the single point the control was worth.

This project implements that subtraction model against whatever subset of
controls is loaded. The maximum here is the sum of loaded control points, not
110, and the report says so plainly. Do not present a subset score as a full
110-control SPRS result.
"""


def score(results):
    """Compute an SPRS-style score from a list of evaluated control results.

    Each result is a dict with at least 'status' and 'weight'. 'manual' controls
    are not counted as failures; they are surfaced separately for human review.
    """
    max_points = sum(r["weight"] for r in results)
    deductions = sum(r["weight"] for r in results if r["status"] == "fail")

    passed = [r for r in results if r["status"] == "pass"]
    failed = [r for r in results if r["status"] == "fail"]
    manual = [r for r in results if r["status"] == "manual"]

    return {
        "max_points": max_points,
        "deductions": deductions,
        "sprs_score": max_points - deductions,
        "controls_total": len(results),
        "controls_passed": len(passed),
        "controls_failed": len(failed),
        "controls_manual": len(manual),
        "percent_met": round(100 * len(passed) / len(results), 1) if results else 0.0,
    }
