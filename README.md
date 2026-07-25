# ComplyScan

Automated NIST SP 800-171 assessment with SPRS-style scoring and POA&M
generation. Feed it a machine-readable description of a system and a control
catalog, and it tells you which controls are met, computes a score, and produces
the two artifacts a compliance analyst actually delivers: an assessment report
and a Plan of Action and Milestones.

This is the GRC and compliance-automation side of security. It maps directly to
the kind of NIST 800-171 and CMMC work that defense contractors have to do to
hold contracts involving Controlled Unclassified Information (CUI).

## Why this matters

Any company in the DoD supply chain that handles CUI has to self-assess against
the 110 controls in NIST SP 800-171 and post a score in DoD's Supplier
Performance Risk System (SPRS). That assessment starts at 110 and subtracts a
weighted value (1, 3, or 5) for every control that is not met. Doing this by hand
across many systems is slow and error-prone. ComplyScan turns the control logic
into code so an assessment is repeatable and reviewable.

## Quick start

```bash
pip install -r requirements.txt
python -m complyscan \
    --system sample_system/system_config.yaml \
    --controls controls/nist_800_171_r2.yaml \
    --report assessment.md \
    --poam poam.csv
```

Console output:

```
ComplyScan  |  Cardinal Ridge Technologies - CUI Enclave
SPRS-style score: 65 of 85   (16 met, 6 not met, 1 manual)
Report written to assessment.md
POA&M written to poam.csv  (7 open items)
```

- `assessment.md` groups every control by family with a met / not met / review
  status.
- `poam.csv` lists each gap with a suggested fix and a target date derived from
  the control's weight (heavier gaps get tighter deadlines). It opens in Excel.

## How scoring works

The SPRS methodology is a subtraction model:

```
score = (sum of loaded control points) - (sum of weights for unmet controls)
```

Controls that need a human decision (policy and procedural items) are reported
as `manual` and are not silently counted as passing. See `complyscan/scoring.py`
for the implementation and `complyscan/checks.py` for how each control is
evaluated.

## Defining a control

Controls live in `controls/nist_800_171_r2.yaml`. Each one names a place in the
system description and states the compliant value:

```yaml
- id: "3.5.3"
  family: Identification and Authentication
  title: Use multifactor authentication for network and privileged access
  weight: 5
  check: { key: identity.mfa_enabled, equals: true }
  remediation: Enforce MFA for all remote and privileged access.
```

Supported check operators: `equals`, `min`, `max`, `one_of`, `contains`,
`exists`, and `manual`.

## Describing a system

The system file (`sample_system/system_config.yaml`) is a nested map of observed
settings. In a real assessment these values come from configuration exports and
evidence collection; here they are hand-written so the sample produces a
realistic mix of passes and failures.

## Tests

```bash
python tests/test_assessor.py     # no dependencies
# or
python -m pytest -q
```

## Honest scope

The control catalog is a curated subset of 800-171 Rev 2, not all 110 controls,
so the maximum score here is the sum of loaded control points rather than 110.
The report states this on its face. The point weights follow the DoD Assessment
Methodology model, but a real submission still requires a qualified assessor and
evidence review. This tool automates the mechanical scoring and documentation, not the
professional judgment around it.

## Layout

```
complyscan/       assessor, check operators, SPRS scoring, POA&M, report, CLI
controls/         NIST 800-171 Rev 2 control catalog (subset) with weights
sample_system/    example system description
tests/            unit tests for checks and scoring
```
