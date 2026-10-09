import unittest

from src.stage2.normalize_data import TRANSDUCERS, canonical_order, normalize, normalize_one


class NormalizationTests(unittest.TestCase):
    def test_ml_equivalent_names_have_one_canonical_token(self):
        for term in ("sklearn", "Scikit-learn", "SCIKIT   LEARN"):
            with self.subTest(term=term):
                self.assertEqual(normalize_one(term, "machine_learning"), "SCIKIT_LEARN")

    def test_architect_equivalent_names(self):
        cases = {"Modelado de datos": "DATA_MODELING", "Data Modelling": "DATA_MODELING",
                 "Google BigQuery": "BIGQUERY", "Amazon Web Services": "AWS", "Apache Kafka": "KAFKA"}
        for term, expected in cases.items():
            with self.subTest(term=term):
                self.assertEqual(normalize_one(term, "data_architect"), expected)

    def test_fst_really_performs_the_translation(self):
        self.assertEqual(list(TRANSDUCERS["data_architect"].translate(["amazon web services"])), [["AWS"]])
        self.assertEqual(list(TRANSDUCERS["machine_learning"].translate(["unknown"])), [])

    def test_unrecognized_terms_are_reported(self):
        canonical, unknown = normalize(["Python", "Excel"], "machine_learning")
        self.assertEqual(canonical, ["PYTHON"])
        self.assertEqual(unknown, ["Excel"])

    def test_alias_duplicates_do_not_add_qualifications(self):
        canonical, unknown = normalize(["sklearn", "Scikit-learn", "Python"], "machine_learning")
        self.assertEqual(canonical, ["SCIKIT_LEARN", "PYTHON"])
        self.assertEqual(unknown, [])

    def test_categories_define_the_canonical_order(self):
        self.assertEqual(canonical_order(["GIT", "SQL", "SCIKIT_LEARN", "NUMPY", "PYTHON"], "machine_learning"),
                         ["PYTHON", "NUMPY", "SCIKIT_LEARN", "SQL", "GIT"])

    def test_database_names_are_not_renamed_to_sql(self):
        self.assertEqual(normalize_one("Postgres", "machine_learning"), "POSTGRESQL")


if __name__ == "__main__":
    unittest.main()
