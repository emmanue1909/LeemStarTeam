import unittest

from src.stage3.classify_data import AUTOMATA, classify

ML = ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]
ARCHITECT = ["DATA_MODELING", "SNOWFLAKE", "AIRFLOW", "AWS", "PYTHON", "SQL", "GIT"]


class ClassificationTests(unittest.TestCase):
    def test_official_ml_automaton_example(self):
        self.assertTrue(classify(ML, "machine_learning")["accepted"])

    def test_data_architect_is_accepted(self):
        self.assertTrue(classify(ARCHITECT, "data_architect")["accepted"])

    def test_each_missing_ml_category_is_rejected(self):
        for token in ML:
            with self.subTest(token=token):
                result = classify([t for t in ML if t != token], "machine_learning")
                self.assertFalse(result["accepted"])
                self.assertEqual(len(result["missing_categories"]), 1)

    def test_each_missing_architect_category_is_rejected(self):
        for token in ARCHITECT:
            with self.subTest(token=token):
                self.assertFalse(classify([t for t in ARCHITECT if t != token], "data_architect")["accepted"])

    def test_alternatives_in_same_category_are_allowed(self):
        tokens = ["PYTHON", "PANDAS", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "SQL", "GIT"]
        self.assertTrue(classify(tokens, "machine_learning")["accepted"])

    def test_empty_and_unknown_input_are_rejected(self):
        self.assertFalse(classify([], "machine_learning")["accepted"])
        self.assertFalse(classify(ML + ["UNKNOWN"], "machine_learning")["accepted"])

    def test_dfa_rejects_noncanonical_order(self):
        self.assertFalse(classify(list(reversed(ML)), "machine_learning")["accepted"])

    def test_traces_end_at_the_accepting_state(self):
        result = classify(ARCHITECT, "data_architect")
        self.assertEqual(result["trace"][0], {"from": "q0", "symbol": "DATA_MODELING", "to": "q1"})
        self.assertEqual(result["trace"][-1]["to"], "q7")

    def test_models_are_deterministic(self):
        for dfa in AUTOMATA.values():
            self.assertTrue(dfa.is_deterministic())


if __name__ == "__main__":
    unittest.main()
