"""
Tests for ComplyScan check evaluation and scoring.

Run from the project root:
    python tests/test_assessor.py
    # or
    python -m pytest -q
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from complyscan.checks import evaluate, resolve
from complyscan.scoring import score
from complyscan.assessor import assess


SYSTEM = {
    "identity": {"mfa_enabled": True, "min_password_length": 14},
    "audit": {"log_retention_days": 45},
    "config_mgmt": {"hardening_standard": "CIS"},
}


def test_resolve_finds_nested_value():
    found, value = resolve(SYSTEM, "identity.mfa_enabled")
    assert found and value is True


def test_resolve_reports_missing_path():
    found, _ = resolve(SYSTEM, "identity.nope")
    assert not found


def test_equals_check():
    assert evaluate({"key": "identity.mfa_enabled", "equals": True}, SYSTEM) == "pass"


def test_min_check_fails_below_threshold():
    assert evaluate({"key": "audit.log_retention_days", "min": 90}, SYSTEM) == "fail"


def test_min_check_passes_at_or_above():
    assert evaluate({"key": "identity.min_password_length", "min": 12}, SYSTEM) == "pass"


def test_one_of_check():
    assert evaluate({"key": "config_mgmt.hardening_standard", "one_of": ["CIS", "STIG"]}, SYSTEM) == "pass"


def test_missing_key_is_a_failure_not_an_error():
    assert evaluate({"key": "identity.absent", "equals": True}, SYSTEM) == "fail"


def test_manual_check_is_flagged_for_review():
    assert evaluate({"manual": True}, SYSTEM) == "manual"


def test_scoring_subtracts_weights_of_failures():
    results = [
        {"status": "pass", "weight": 5},
        {"status": "fail", "weight": 3},
        {"status": "fail", "weight": 1},
        {"status": "manual", "weight": 3},
    ]
    summary = score(results)
    assert summary["max_points"] == 12
    assert summary["deductions"] == 4          # 3 + 1
    assert summary["sprs_score"] == 8          # 12 - 4
    assert summary["controls_manual"] == 1     # manual not counted as failure


def test_assess_integrates_checks_and_scoring():
    controls = [
        {"id": "3.5.3", "family": "IA", "title": "MFA", "weight": 5,
         "check": {"key": "identity.mfa_enabled", "equals": True}},
        {"id": "3.3.8", "family": "AU", "title": "retention", "weight": 3,
         "check": {"key": "audit.log_retention_days", "min": 90}},
    ]
    results, summary = assess(controls, SYSTEM)
    statuses = {r["id"]: r["status"] for r in results}
    assert statuses["3.5.3"] == "pass"
    assert statuses["3.3.8"] == "fail"
    assert summary["sprs_score"] == 5          # 8 possible minus 3 for the fail


def _run_all():
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok  -", name)
            passed += 1
    print("\n%d tests passed" % passed)


if __name__ == "__main__":
    _run_all()
