import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.data_app import main, process_file

ROOT = Path(__file__).resolve().parents[2]


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "tests/data_profiles")
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "results"

    def source(self, name):
        return ROOT / "examples/data_profiles" / name

    def test_both_profiles_are_exported_in_one_candidate(self):
        report = process_file(self.source("ml_and_architect.txt"), self.output)
        self.assertEqual(report["export_status"], "VALID")
        self.assertEqual(json.loads((self.output / "report.json").read_text(encoding="utf-8")), report)
        self.assertIn("classification Data Architect", (self.output / "candidate.resume").read_text(encoding="utf-8"))
        self.assertIn("Lucía Moreno Rojas", (self.output / "candidate.md").read_text(encoding="utf-8"))

    def test_rejected_candidate_is_reported_without_visualization(self):
        report = process_file(self.source("ml_incomplete.txt"), self.output, "machine_learning")
        self.assertEqual(report["export_status"], "NOT_ACCEPTED")
        self.assertFalse((self.output / "candidate.resume").exists())
        self.assertFalse((self.output / "candidate.md").exists())

    def test_missing_levels_block_export_but_keep_the_automaton_result(self):
        source = Path(self.temp.name) / "missing_levels.txt"
        source.write_text(self.source("ml_engineer.txt").read_text(encoding="utf-8").replace("Python (nivel 4)", "Python"), encoding="utf-8")
        report = process_file(source, self.output, "machine_learning")
        self.assertTrue(report["profiles"]["machine_learning"]["accepted"])
        self.assertEqual(report["export_status"], "BLOCKED")
        self.assertFalse((self.output / "candidate.md").exists())

    def test_existing_outputs_are_not_overwritten(self):
        process_file(self.source("ml_engineer.txt"), self.output)
        previous = (self.output / "report.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "not be overwritten"):
            process_file(self.source("ml_incomplete.txt"), self.output)
        self.assertEqual((self.output / "report.json").read_bytes(), previous)

    def test_missing_input_does_not_create_outputs(self):
        with self.assertRaises(FileNotFoundError):
            process_file(Path(self.temp.name) / "missing.txt", self.output)
        self.assertFalse(self.output.exists())

    def test_console_summary_reports_status_and_missing_categories(self):
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            code = main([str(self.source("ml_incomplete.txt")), "--profile", "machine_learning", "--output-dir", str(self.output)])
        self.assertEqual(code, 0)
        self.assertIn("REJECTED", capture.getvalue())
        self.assertIn("Machine learning library", capture.getvalue())

    def test_cli_works_from_a_different_directory(self):
        command = [sys.executable, "-m", "src.data_app", str(self.source("ml_and_architect.txt")), "--output-dir", str(self.output)]
        environment = dict(os.environ, PYTHONPATH=str(ROOT), PYTHONIOENCODING="utf-8")
        completed = subprocess.run(command, cwd=self.temp.name, env=environment, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Candidate export: VALID", completed.stdout)


if __name__ == "__main__":
    unittest.main()
