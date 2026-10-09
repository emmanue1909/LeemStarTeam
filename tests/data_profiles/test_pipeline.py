import random
import tempfile
import unittest
from pathlib import Path

from src.data_pipeline import candidate_documents, evaluate_profiles, run_pipeline, to_dsl
from src.stage4.validator import mm, validate
from src.stage4.markdown_generator import parse_file, render_markdown

ROOT = Path(__file__).resolve().parents[2]


class PipelineTests(unittest.TestCase):
    def source(self, filename):
        return (ROOT / "examples/data_profiles" / filename).read_text(encoding="utf-8")

    def test_both_complete_examples_pass_all_three_stages(self):
        for profile, filename in (("machine_learning", "ml_engineer.txt"), ("data_architect", "data_architect.txt")):
            with self.subTest(profile=profile):
                result = run_pipeline(self.source(filename), profile)
                self.assertTrue(result["accepted"])
                self.assertEqual(result["missing_categories"], [])
                self.assertIn("qualification", to_dsl(result, profile))

    def test_incomplete_examples_are_rejected(self):
        for profile, filename, missing in (("machine_learning", "ml_incomplete.txt", "Machine learning library"),
                                           ("data_architect", "data_architect_incomplete.txt", "Data modeling")):
            with self.subTest(profile=profile):
                result = run_pipeline(self.source(filename), profile)
                self.assertFalse(result["accepted"])
                self.assertEqual(result["missing_categories"], [missing])
                with self.assertRaises(ValueError):
                    to_dsl(result, profile)

    def test_resume_order_does_not_change_classification(self):
        terms = ["Git", "SQL", "Python", "Pandas", "sklearn"]
        rng = random.Random(7)
        for _ in range(20):
            rng.shuffle(terms)
            result = run_pipeline("Skills: " + ", ".join(terms), "machine_learning")
            self.assertTrue(result["accepted"])
            self.assertEqual(result["qualifications"], ["PYTHON", "PANDAS", "SCIKIT_LEARN", "SQL", "GIT"])

    def test_ml_export_parses_with_existing_grammar_and_renders(self):
        result = run_pipeline(self.source("ml_engineer.txt"), "machine_learning")
        with tempfile.TemporaryDirectory(dir=ROOT / "tests/data_profiles") as folder:
            path = Path(folder) / "ml.resume"
            path.write_text(to_dsl(result, "machine_learning"), encoding="utf-8")
            model = parse_file(path)
        self.assertEqual(model.classifications[0].label, "Machine Learning Engineer")
        markdown = render_markdown(model)
        self.assertIn("Julián Restrepo", markdown)
        self.assertIn("SCIKIT_LEARN", markdown)
        self.assertIn("(level 3)", markdown)

    def test_data_architect_export_has_the_agreed_label(self):
        result = run_pipeline(self.source("data_architect.txt"), "data_architect")
        self.assertIn("classification Data Architect", to_dsl(result, "data_architect"))

    def test_architect_export_is_valid_and_visualized(self):
        dsl, markdown = candidate_documents(evaluate_profiles(self.source("data_architect.txt")))
        self.assertEqual(validate(mm.model_from_str(dsl)), [])
        self.assertIn("Data Architect", markdown)
        self.assertIn("DATA_MODELING", markdown)

    def test_multiple_accepted_profiles_are_preserved(self):
        results = evaluate_profiles(self.source("ml_and_architect.txt"))
        self.assertTrue(all(result["accepted"] for result in results.values()))
        dsl, markdown = candidate_documents(results)
        model = mm.model_from_str(dsl)
        self.assertEqual([item.label for item in model.classifications], ["Machine Learning Engineer", "Data Architect"])
        self.assertEqual(validate(model), [])
        self.assertEqual(len(model.skills), len({item.name for item in model.skills}))
        self.assertIn("Machine Learning Engineer, Data Architect", markdown)

    def test_accepted_pattern_does_not_bypass_business_validation(self):
        text = self.source("ml_engineer.txt")
        results = evaluate_profiles(text)
        results["machine_learning"]["extracted"]["educations"][0]["phone"] = "5551234"
        with self.assertRaisesRegex(ValueError, "Invalid candidate profile"):
            candidate_documents(results)

    def test_different_candidates_cannot_be_combined(self):
        results = {"machine_learning": run_pipeline(self.source("ml_engineer.txt"), "machine_learning"),
                   "data_architect": run_pipeline(self.source("data_architect.txt"), "data_architect")}
        with self.assertRaisesRegex(ValueError, "different candidates"):
            candidate_documents(results)

    def test_result_profile_cannot_be_mislabeled(self):
        result = run_pipeline(self.source("ml_engineer.txt"), "machine_learning")
        with self.assertRaisesRegex(ValueError, "do not match"):
            to_dsl(result, "data_architect")

    def test_proficiency_levels_are_not_invented(self):
        text = self.source("ml_engineer.txt").replace("Python (nivel 4)", "Python")
        result = run_pipeline(text, "machine_learning")
        self.assertTrue(result["accepted"])
        with self.assertRaisesRegex(ValueError, "Missing declared levels"):
            to_dsl(result, "machine_learning")

    def test_conflicting_alias_levels_are_rejected(self):
        text = self.source("ml_engineer.txt") + "\nSkills: Scikit-learn (nivel 5)."
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            to_dsl(run_pipeline(text, "machine_learning"), "machine_learning")

    def test_invalid_level_is_rejected(self):
        text = self.source("ml_engineer.txt").replace("Python (nivel 4)", "Python (nivel 9)")
        with self.assertRaisesRegex(ValueError, "outside 1..5"):
            to_dsl(run_pipeline(text, "machine_learning"), "machine_learning")

    def test_identity_is_not_fabricated_to_fill_the_dsl(self):
        text = "Skills: Python, Pandas, sklearn, SQL, Git."
        with self.assertRaisesRegex(ValueError, "Missing candidate information"):
            to_dsl(run_pipeline(text, "machine_learning"), "machine_learning")

    def test_english_examples_complete_the_same_pipeline(self):
        for filename, profile in (("ml_english.txt", "machine_learning"), ("architect_english.txt", "data_architect")):
            with self.subTest(profile=profile):
                dsl, markdown = candidate_documents({profile: run_pipeline(self.source(filename), profile)})
                self.assertEqual(validate(mm.model_from_str(dsl)), [])
                self.assertIn("## Experience", markdown)


if __name__ == "__main__":
    unittest.main()
