"""Render the assessment as a Markdown report an auditor can read."""

from collections import defaultdict


_STATUS_MARK = {"pass": "MET", "fail": "NOT MET", "manual": "REVIEW"}


def markdown_report(results, summary, system_name):
    """Build a Markdown compliance report from results and the score summary."""
    lines = []
    lines.append("# NIST SP 800-171 Assessment Report")
    lines.append("")
    lines.append("**System:** %s" % system_name)
    lines.append("")
    lines.append("## Score summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append("| SPRS-style score | **%d** of %d possible |"
                 % (summary["sprs_score"], summary["max_points"]))
    lines.append("| Point deductions | %d |" % summary["deductions"])
    lines.append("| Controls assessed | %d |" % summary["controls_total"])
    lines.append("| Met | %d |" % summary["controls_passed"])
    lines.append("| Not met | %d |" % summary["controls_failed"])
    lines.append("| Manual review | %d |" % summary["controls_manual"])
    lines.append("| Percent met (automated) | %.1f%% |" % summary["percent_met"])
    lines.append("")
    lines.append("> Scored against a representative subset of controls, not all "
                 "110. The maximum shown is the sum of loaded control points.")
    lines.append("")

    # Group results by control family for readability.
    by_family = defaultdict(list)
    for result in results:
        by_family[result["family"]].append(result)

    lines.append("## Findings by control family")
    lines.append("")
    for family in sorted(by_family):
        lines.append("### %s" % family)
        lines.append("")
        lines.append("| Control | Title | Result | Weight |")
        lines.append("|---------|-------|--------|--------|")
        for result in sorted(by_family[family], key=lambda r: r["id"]):
            lines.append("| %s | %s | %s | %d |" % (
                result["id"],
                result["title"],
                _STATUS_MARK[result["status"]],
                result["weight"],
            ))
        lines.append("")

    open_items = [r for r in results if r["status"] in ("fail", "manual")]
    if open_items:
        lines.append("## Open items")
        lines.append("")
        lines.append("The following controls need remediation or review. See the "
                     "generated POA&M for target dates.")
        lines.append("")
        for result in sorted(open_items, key=lambda r: (-r["weight"], r["id"])):
            lines.append("- **%s (%s, weight %d)** — %s"
                         % (result["id"], _STATUS_MARK[result["status"]],
                            result["weight"],
                            result["remediation"] or "Corrective action required."))
        lines.append("")

    return "\n".join(lines)
