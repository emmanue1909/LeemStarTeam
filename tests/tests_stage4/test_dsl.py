import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from textx.exceptions import TextXSyntaxError
from src.stage4.validator import mm, validate

ROOT = Path(__file__).resolve().parent


def check(path):
    """True if `path` parses against the grammar AND satisfies every rule in validator.py."""
    try:
        model = mm.model_from_file(str(path), encoding="utf-8")
    except TextXSyntaxError:
        return False
    return len(validate(model)) == 0


class DslTests(unittest.TestCase):
    def test_valid_resumes_are_accepted(self):
        for path in sorted((ROOT / "valid").glob("*.resume")):
            with self.subTest(file=path.name):
                self.assertTrue(check(path))

    def test_invalid_resumes_are_rejected(self):
        for path in sorted((ROOT / "invalid").glob("*.resume")):
            with self.subTest(file=path.name):
                self.assertFalse(check(path))


if __name__ == "__main__":
    unittest.main()
