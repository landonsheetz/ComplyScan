# NIST SP 800-171 Assessment Report

**System:** Cardinal Ridge Technologies - CUI Enclave

## Score summary

| Metric | Value |
|--------|-------|
| SPRS-style score | **65** of 85 possible |
| Point deductions | 20 |
| Controls assessed | 23 |
| Met | 16 |
| Not met | 6 |
| Manual review | 1 |
| Percent met (automated) | 69.6% |

> Scored against a representative subset of controls, not all 110. The maximum shown is the sum of loaded control points.

## Findings by control family

### Access Control

| Control | Title | Result | Weight |
|---------|-------|--------|--------|
| 3.1.1 | Limit system access to authorized users and processes | MET | 5 |
| 3.1.12 | Monitor and control remote access sessions | MET | 5 |
| 3.1.2 | Limit access to the functions users are permitted to execute | MET | 5 |
| 3.1.20 | Control connections to external systems | NOT MET | 1 |
| 3.1.5 | Employ least privilege for privileged accounts | NOT MET | 3 |

### Audit and Accountability

| Control | Title | Result | Weight |
|---------|-------|--------|--------|
| 3.3.1 | Create and retain system audit logs | MET | 5 |
| 3.3.2 | Ensure actions are traceable to individual users | MET | 3 |
| 3.3.8 | Protect audit information from unauthorized access | NOT MET | 3 |

### Awareness and Training

| Control | Title | Result | Weight |
|---------|-------|--------|--------|
| 3.2.1 | Ensure personnel are trained on security risks | REVIEW | 3 |

### Configuration Management

| Control | Title | Result | Weight |
|---------|-------|--------|--------|
| 3.4.1 | Establish and maintain baseline configurations | MET | 5 |
| 3.4.2 | Enforce security configuration settings | MET | 3 |
| 3.4.6 | Apply the principle of least functionality | NOT MET | 3 |

### Identification and Authentication

| Control | Title | Result | Weight |
|---------|-------|--------|--------|
| 3.5.10 | Store and transmit only cryptographically protected passwords | MET | 5 |
| 3.5.3 | Use multifactor authentication for network and privileged access | MET | 5 |
| 3.5.7 | Enforce minimum password complexity | MET | 1 |

### Incident Response

| Control | Title | Result | Weight |
|---------|-------|--------|--------|
| 3.6.1 | Establish an operational incident-handling capability | MET | 5 |
| 3.6.2 | Track and report incidents to designated officials | MET | 3 |

### Risk Assessment

| Control | Title | Result | Weight |
|---------|-------|--------|--------|
| 3.11.2 | Scan for vulnerabilities periodically | NOT MET | 5 |
| 3.11.3 | Remediate vulnerabilities in line with risk assessments | MET | 1 |

### System and Communications Protection

| Control | Title | Result | Weight |
|---------|-------|--------|--------|
| 3.13.11 | Use FIPS-validated cryptography to protect CUI | NOT MET | 5 |
| 3.13.16 | Protect the confidentiality of CUI at rest | MET | 1 |

### System and Information Integrity

| Control | Title | Result | Weight |
|---------|-------|--------|--------|
| 3.14.1 | Identify and correct system flaws promptly | MET | 5 |
| 3.14.2 | Provide protection from malicious code | MET | 5 |

## Open items

The following controls need remediation or review. See the generated POA&M for target dates.

- **3.11.2 (NOT MET, weight 5)** — Scan for vulnerabilities at least every 30 days.
- **3.13.11 (NOT MET, weight 5)** — Use FIPS 140-validated cryptographic modules for CUI.
- **3.1.5 (NOT MET, weight 3)** — Review privileged accounts at least every 90 days.
- **3.2.1 (REVIEW, weight 3)** — Retain security awareness training records for review.
- **3.3.8 (NOT MET, weight 3)** — Retain protected audit logs for at least 90 days.
- **3.4.6 (NOT MET, weight 3)** — Disable unnecessary ports, protocols, and services.
- **3.1.20 (NOT MET, weight 1)** — Define and enforce an external connection policy.
