"""Regression tests for the program risk board."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from program_risk_board.analysis import analyze_risks
from program_risk_board.cli import run
from program_risk_board.data import load_risks


DATA_FILE = ROOT / "data" / "risks.json"


class RiskBoardTests(unittest.TestCase):
    def test_clean_dataset_passes(self) -> None:
        result = analyze_risks(load_risks(DATA_FILE))
        self.assertEqual(result.errors, [])
        self.assertEqual(result.summary["risk_count"], 5)

    def test_invalid_scale_value_is_detected(self) -> None:
        risks = load_risks(DATA_FILE)
        risks[0]["severity"] = 11
        result = analyze_risks(risks)
        self.assertTrue(any("severity must be an integer between 1 and 10" in message for message in result.errors))

    def test_cli_exports_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = run(["analyze", "--data-file", str(DATA_FILE), "--export-dir", temp_dir])
            self.assertEqual(exit_code, 0)
            export_dir = Path(temp_dir)
            self.assertTrue((export_dir / "risk-summary.md").exists())
            self.assertTrue((export_dir / "risk-register.csv").exists())
            self.assertTrue((export_dir / "risk-gate-matrix.csv").exists())
            self.assertTrue((export_dir / "risk-dashboard.html").exists())


if __name__ == "__main__":
    unittest.main()
