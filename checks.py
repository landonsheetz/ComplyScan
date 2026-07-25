"""
Check evaluation.

A control definition points at a place in the system description and says what a
compliant value looks like. This module resolves that path and decides whether
the observed value passes.

Supported check operators:

    equals: <value>        observed value must equal this exactly
    min: <number>          observed value must be >= this (e.g. password length)
    max: <number>          observed value must be <= this (e.g. session timeout)
    one_of: [a, b]         observed value must be in this list
    contains: <value>      observed list/string must contain this
    exists: true           the key must be present and truthy
    manual: true           control cannot be checked automatically; needs review
"""


def resolve(system, dotted_key):
    """Walk a dotted path like 'access_control.mfa_enabled' into a nested dict.

    Returns (found, value). found is False when any segment is missing, which
    lets a control be scored as a failure rather than raising.
    """
    node = system
    for part in dotted_key.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return False, None
    return True, node


def evaluate(check, system):
    """Return one of: 'pass', 'fail', 'manual'.

    A control with no automatable check is reported as 'manual' so the assessor
    can flag it for a human instead of guessing. That mirrors how real 800-171
    assessments handle policy and procedural controls.
    """
    if check.get("manual"):
        return "manual"

    key = check.get("key")
    if key is None:
        return "manual"

    found, value = resolve(system, key)

    if "exists" in check:
        return "pass" if (found and bool(value)) else "fail"

    if not found:
        return "fail"

    if "equals" in check:
        return "pass" if value == check["equals"] else "fail"

    if "min" in check:
        try:
            return "pass" if float(value) >= float(check["min"]) else "fail"
        except (TypeError, ValueError):
            return "fail"

    if "max" in check:
        try:
            return "pass" if float(value) <= float(check["max"]) else "fail"
        except (TypeError, ValueError):
            return "fail"

    if "one_of" in check:
        return "pass" if value in check["one_of"] else "fail"

    if "contains" in check:
        try:
            return "pass" if check["contains"] in value else "fail"
        except TypeError:
            return "fail"

    # A check with a key but no recognized operator is treated as manual rather
    # than silently passing.
    return "manual"
