import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

from src.data_app import analyze_text

ROOT = Path(__file__).resolve().parents[2]


class WebTests(unittest.TestCase):
    def app(self):
        return AppTest.from_file(str(ROOT / "src/data_web.py"), default_timeout=15).run()

    def test_combined_candidate_is_shown_and_downloadable(self):
        app = self.app()
        app.button[0].click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn("Candidate export: VALID", [item.value for item in app.markdown])
        self.assertEqual(len(app.get("download_button")), 3)
        self.assertIn("Machine Learning Engineer, Data Architect", app.markdown[-1].value)

    def test_rejected_candidate_has_no_candidate_download(self):
        app = self.app()
        app.text_area[0].set_value("Skills: Python, SQL, Git")
        app.selectbox[0].set_value("machine_learning")
        app.button[0].click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.get("download_button")), 1)
        self.assertIn("Candidate export: NOT_ACCEPTED", [item.value for item in app.markdown])

    def test_missing_levels_block_visualization_not_pattern(self):
        app = self.app()
        text = (ROOT / "examples/data_profiles/ml_engineer.txt").read_text(encoding="utf-8")
        app.text_area[0].set_value(text.replace("Python (nivel 4)", "Python"))
        app.selectbox[0].set_value("machine_learning")
        app.button[0].click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.get("download_button")), 1)
        self.assertIn("Missing declared levels", app.warning[0].value)

    def test_changed_input_does_not_show_stale_downloads(self):
        app = self.app()
        app.button[0].click().run()
        app.text_area[0].set_value("Other text").run()
        self.assertEqual(len(app.get("download_button")), 0)
        self.assertIn("Inputs changed", app.info[0].value)

    def test_empty_text_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Enter résumé text"):
            analyze_text(" \n ")
        app = self.app()
        app.text_area[0].set_value("")
        app.button[0].click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertIn("Enter résumé text", app.error[0].value)


if __name__ == "__main__":
    unittest.main()
