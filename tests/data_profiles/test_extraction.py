import unittest
from pathlib import Path

from src.stage1.extract_data import extract, extract_qualifications

ROOT = Path(__file__).resolve().parents[2]


class ExtractionTests(unittest.TestCase):
    def test_ml_raw_terms_keep_their_spelling(self):
        terms = extract_qualifications("Skills: Python, NumPy, sklearn, Py Torch, SQL, Git.", "machine_learning")
        self.assertEqual(terms, ["Python", "NumPy", "sklearn", "Py Torch", "SQL", "Git"])

    def test_architect_longest_alias_is_one_term(self):
        terms = extract_qualifications("Skills: Apache Spark, Google Cloud Platform, Amazon Redshift.", "data_architect")
        self.assertEqual(terms, ["Apache Spark", "Google Cloud Platform", "Amazon Redshift"])

    def test_word_boundaries_avoid_other_products(self):
        text = "Pythonista, SQLAlchemy, NoSQL, GitHub, GitLab, PandasExtra"
        self.assertEqual(extract_qualifications(text, "machine_learning"), [])

    def test_contact_values_are_not_qualification_claims(self):
        text = "python@example.com https://example.com/Python"
        self.assertEqual(extract_qualifications(text, "machine_learning"), [])

    def test_case_and_spaces_are_preserved(self):
        self.assertEqual(extract_qualifications("SCIKIT   LEARN", "machine_learning"), ["SCIKIT   LEARN"])

    def test_accented_candidate_and_complete_records(self):
        result = extract((ROOT / "examples/data_profiles/ml_engineer.txt").read_text(encoding="utf-8"), "machine_learning")
        self.assertEqual(result["name"], "Julián Restrepo")
        self.assertEqual(result["location"], "Cali, Colombia")
        self.assertEqual(result["email"], "julian.restrepo@example.com")
        self.assertEqual(result["github"], "julianrestrepo")
        self.assertEqual(result["experiences"][0]["years"], 3)
        self.assertEqual(result["educations"][0]["phone"], "+57-2-5559876")
        self.assertEqual(len(result["declared_levels"]), 6)

    def test_multiple_experiences_and_education_records(self):
        text = (
            "Ana Pérez\nMi posición es Analyst en la compañía Uno; tengo 2 años de experiencia.\n"
            "Mi posición es Engineer en la compañía Dos; tengo 1 año de experiencia.\n"
            "Egresada del programa de Sistemas de la Universidad Uno; teléfono institucional +57-2-5559876.\n"
            "Egresada del programa de Datos de la Universidad Dos; teléfono institucional +57-2-5559877."
        )
        data = extract(text, "machine_learning")
        self.assertEqual([job["company"] for job in data["experiences"]], ["Uno", "Dos"])
        self.assertEqual(len(data["educations"]), 2)

    def test_missing_fields_remain_missing(self):
        data = extract("Skills: Python", "machine_learning")
        self.assertIsNone(data["name"])
        self.assertIsNone(data["email"])
        self.assertEqual(data["experiences"], [])

    def test_english_candidate_records(self):
        text = ("Mary Jane Watson\nBased in Cali, Colombia.\n"
                "My position is ML Engineer at Acme; I have 2 years of experience.\n"
                "Graduate of the program Computer Science at Icesi University; institution phone +57-2-5559876.")
        data = extract(text, "machine_learning")
        self.assertEqual(data["location"], "Cali, Colombia")
        self.assertEqual(data["experiences"], [{"position": "ML Engineer", "company": "Acme", "years": 2}])
        self.assertEqual(data["educations"][0]["program"], "Computer Science")

    def test_partial_experience_is_preserved_without_inventing_a_job(self):
        phrase = "2 years of experience developing predictive models"
        data = extract("Mary Jane Watson\n" + phrase + ".", "machine_learning")
        self.assertEqual(data["experience_mentions"], [phrase])
        self.assertEqual(data["experiences"], [])


if __name__ == "__main__":
    unittest.main()
