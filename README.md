# Program Risk Board

`Program Risk Board` is a systems engineering portfolio repository focused on program-level risk review. It turns multi-repository technical and integration risks into structured data, validates scoring consistency, and exports reviewer-facing decision artifacts.

This repo is designed to sit above subsystem analyses. It answers questions like:

- Which risks still threaten review readiness?
- Which workstreams are driving the highest residual exposure?
- Which review gates are carrying the largest open burden?

## What This Repo Demonstrates

- program-level risk aggregation
- residual risk scoring and prioritization
- review-board style exports
- clean automation, tests, and CI

## Repository Map

```text
.
|-- data/                      # Structured risk records
|-- docs/                      # Process notes and build plan
|-- reports/                   # Generated summaries and dashboards
|-- src/program_risk_board/    # Validation, analysis, export, and CLI logic
|-- tests/                     # Regression tests
|-- .github/workflows/         # CI pipeline
|-- Makefile                   # Common commands
`-- README.md
```

## Quick Start

```bash
make test
make analyze
```

Or run the CLI directly:

```bash
PYTHONPATH=src python3 -m program_risk_board.cli analyze --data-file data/risks.json --export-dir reports
```

## Generated Outputs

- `reports/risk-summary.md`
- `reports/risk-register.csv`
- `reports/risk-gate-matrix.csv`
- `reports/risk-dashboard.html`

## Documentation

- [docs/README.md](docs/README.md)
- [docs/project_plan.md](docs/project_plan.md)
- [docs/risk_review_process.md](docs/risk_review_process.md)

## Why This Matters For A Recruiter

This repo shows that the portfolio does not stop at component-level logic. It demonstrates how a systems engineer can aggregate open issues, reason about residual exposure, and prepare review-board evidence in a structured, automatable way.
