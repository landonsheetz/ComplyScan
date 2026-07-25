"""
Command-line interface for ComplyScan.

Usage:
    python -m complyscan \\
        --system sample_system/system_config.yaml \\
        --controls controls/nist_800_171_r2.yaml \\
        --report assessment.md \\
        --poam poam.csv
"""

import argparse
import sys

from .assessor import load_controls, load_yaml, assess
from .report import markdown_report
from .poam import build_poam_rows, write_csv


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="complyscan",
        description="Automated NIST SP 800-171 assessment and SPRS scoring.",
    )
    parser.add_argument("--system", required=True, help="YAML system description.")
    parser.add_argument("--controls", default="controls/nist_800_171_r2.yaml",
                        help="YAML control catalog.")
    parser.add_argument("--report", help="Optional path to write a Markdown report.")
    parser.add_argument("--poam", help="Optional path to write a POA&M CSV.")
    parser.add_argument("--min-score", type=int,
                        help="Exit non-zero if the SPRS score is below this value.")
    args = parser.parse_args(argv)

    system_doc = load_yaml(args.system)
    system_name = system_doc.get("system_name", args.system)
    system = system_doc.get("configuration", system_doc)

    controls = load_controls(args.controls)
    results, summary = assess(controls, system)

    print("ComplyScan  |  %s" % system_name)
    print("SPRS-style score: %d of %d   (%d met, %d not met, %d manual)" % (
        summary["sprs_score"], summary["max_points"],
        summary["controls_passed"], summary["controls_failed"],
        summary["controls_manual"],
    ))

    if args.report:
        with open(args.report, "w", encoding="utf-8") as handle:
            handle.write(markdown_report(results, summary, system_name))
        print("Report written to %s" % args.report)

    if args.poam:
        rows = build_poam_rows(results)
        count = write_csv(rows, args.poam)
        print("POA&M written to %s  (%d open items)" % (args.poam, count))

    if args.min_score is not None and summary["sprs_score"] < args.min_score:
        print("Score %d is below the required %d." % (summary["sprs_score"], args.min_score))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
