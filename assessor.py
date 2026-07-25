"""
The assessor: load controls, load a system description, evaluate each control,
and hand back structured results plus a score.
"""

import yaml

from .checks import evaluate
from .scoring import score


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_controls(path):
    """Load the control catalog and validate the fields the assessor relies on."""
    data = load_yaml(path)
    controls = data.get("controls", [])
    for control in controls:
        for field in ("id", "family", "title", "weight", "check"):
            if field not in control:
                raise ValueError(
                    "Control %s is missing required field '%s'"
                    % (control.get("id", "?"), field)
                )
    return controls


def assess(controls, system):
    """Evaluate every control against the system description.

    Returns a list of per-control result dicts and an aggregate score dict.
    """
    results = []
    for control in controls:
        status = evaluate(control["check"], system)
        results.append({
            "id": control["id"],
            "family": control["family"],
            "title": control["title"],
            "weight": control["weight"],
            "status": status,
            "remediation": control.get("remediation", ""),
            "check": control["check"],
        })

    summary = score(results)
    return results, summary
