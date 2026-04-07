"""CLI for the program risk board."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .analysis import analyze_risks
from .data import load_risks
from .export import export_reports


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(
        prog="program-risk-board",
        description="Validate and export program-level risk review artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze", help="Analyze risk records and export reports.")
    analyze_parser.add_argument("--data-file", default="data/risks.json", help="Path to the risk data JSON file.")
    analyze_parser.add_argument("--export-dir", help="Directory where reports should be written.")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "analyze":
        result = analyze_risks(load_risks(Path(args.data_file)))
        _print_summary(result)
        if args.export_dir:
            export_reports(result, Path(args.export_dir))
            print(f"Reports exported to: {args.export_dir}")
        return 1 if result.errors else 0

    parser.error("Unknown command.")
    return 2


def _print_summary(result) -> None:
    summary = result.summary
    print("Program risk summary")
    print(f"  Risks: {summary['risk_count']}")
    print(f"  Open risks: {summary['open_count']}")
    print(f"  Critical residual risks: {summary['critical_count']}")
    print(f"  Review gates: {summary['review_gate_count']}")
    print(f"  Linked repositories: {summary['linked_repo_count']}")
    print(f"  Errors: {summary['error_count']}")
    print(f"  Warnings: {summary['warning_count']}")
    if result.errors:
        print("Validation errors:")
        for message in result.errors:
            print(f"  - {message}")
    if result.warnings:
        print("Validation warnings:")
        for message in result.warnings:
            print(f"  - {message}")


if __name__ == "__main__":
    raise SystemExit(run())
