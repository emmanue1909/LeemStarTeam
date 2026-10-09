import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.stage4.markdown_generator import parse_file
from src.stage4.validator import mm, validate

ROOT = Path(__file__).resolve().parents[2]


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.valid = (ROOT / "examples/resume_01.resume").read_text(encoding="utf-8")

    def test_empty_mandatory_strings_are_rejected(self):
        model = mm.model_from_str(self.valid)
        fields = [(model.personal, "name"), (model.personal, "location"),
                  (model.contact, "email"), (model.experiences[0], "position"),
                  (model.experiences[0], "company"), (model.educations[0], "program"),
                  (model.educations[0], "institution_name"), (model.educations[0], "phone"),
                  (model.skills[0], "name"), (model.qualifications[0], "name")]
        for item, field in fields:
            with self.subTest(field=field):
                previous = getattr(item, field)
                setattr(item, field, "   ")
                self.assertTrue(validate(model))
                setattr(item, field, previous)

    def test_duplicate_qualifications_are_rejected(self):
        model = mm.model_from_str(self.valid)
        model.qualifications.append(model.qualifications[0])
        self.assertTrue(validate(model))

    def test_valid_example_still_passes(self):
        self.assertEqual(validate(mm.model_from_str(self.valid)), [])

    def test_independent_parser_rejects_business_errors(self):
        with self.assertRaises(ValueError):
            parse_file(ROOT / "tests/tests_stage4/invalid/semantic_bad_phone.resume")

    def test_markdown_command_does_not_export_invalid_candidate(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests/data_profiles") as directory:
            output = Path(directory) / "invalid.md"
            completed = subprocess.run(
                [sys.executable, "-m", "src.stage4.markdown_generator",
                 str(ROOT / "tests/tests_stage4/invalid/semantic_bad_phone.resume"),
                 "--output", str(output)],
                cwd=ROOT, env=dict(os.environ, PYTHONIOENCODING="utf-8"),
                capture_output=True, text=True, encoding="utf-8",
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(output.exists())
            self.assertNotIn("Traceback", completed.stderr)


if __name__ == "__main__":
    unittest.main()
