import json
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from src.data_profiles import PROFILES, vocabulary
from src.data_pipeline import candidate_documents, evaluate_profiles, run_pipeline
from src.stage2.normalize_data import TRANSDUCERS
from src.stage3.classify_data import AUTOMATA
from src.stage4.diagram_generator import model_tree, write_tree_dot, write_tree_svg
from src.stage4.validator import parse_validated

ROOT = Path(__file__).resolve().parents[2]
CASES = {"ml_engineer": "machine_learning", "ml_incomplete": "machine_learning",
         "data_architect": "data_architect", "data_architect_incomplete": "data_architect",
         "ml_english": "machine_learning", "architect_english": "data_architect"}
COMPLETE = ["ml_engineer", "data_architect", "ml_english", "architect_english", "ml_and_architect"]


class ArtifactTests(unittest.TestCase):
    def rows(self, profile):
        document = (ROOT / f"docs/data_profiles/{profile}.md").read_text(encoding="utf-8")
        return [[cell.strip() for cell in line.strip("|").split("|")]
                for line in document.splitlines() if line.startswith("|")]

    def test_full_dfa_tables_match_executable_models(self):
        for profile in PROFILES:
            rows = {cells[0].replace("-> ", "").replace("* ", ""): cells[1:]
                    for cells in self.rows(profile)
                    if re.fullmatch(r"(?:-> |\* )?(?:q\d+|q_dead)", cells[0])}
            dfa = AUTOMATA[profile]
            self.assertEqual(set(rows), {str(state.value) for state in dfa.states})
            for state, cells in rows.items():
                self.assertEqual(len(cells), len(vocabulary(profile)))
                for token, target in zip(vocabulary(profile), cells, strict=True):
                    self.assertEqual([str(item.value) for item in dfa(state, token)], [target])

    def test_all_fst_table_rows_match_actual_translations(self):
        for profile, spec in PROFILES.items():
            rows = [(cells[0].strip("`"), cells[1].strip("`")) for cells in self.rows(profile)
                    if len(cells) == 4 and cells[0].startswith("`")]
            self.assertEqual(set(rows), {(alias.casefold(), token)
                                        for token, aliases in spec["variants"].items() for alias in aliases})
            for alias, token in rows:
                self.assertEqual(list(TRANSDUCERS[profile].translate([alias])), [[token]])

    def test_saved_examples_match_current_pipeline(self):
        for name, profile in [*CASES.items(), ("ml_and_architect", None)]:
            with self.subTest(example=name):
                text = (ROOT / f"examples/data_profiles/{name}.txt").read_text(encoding="utf-8")
                results = evaluate_profiles(text) if profile is None else {profile: run_pipeline(text, profile)}
                saved = json.loads((ROOT / f"output/data_profiles/{name}.json").read_text(encoding="utf-8"))
                self.assertEqual(saved, results if profile is None else results[profile])
                if name in COMPLETE:
                    dsl, markdown = candidate_documents(results)
                    self.assertEqual(dsl, (ROOT / f"output/data_profiles/{name}.resume").read_text(encoding="utf-8"))
                    self.assertEqual(markdown, (ROOT / f"output/data_profiles/{name}.md").read_text(encoding="utf-8"))
                else:
                    self.assertFalse(any(result["accepted"] for result in results.values()))
                    self.assertFalse((ROOT / f"output/data_profiles/{name}.resume").exists())

    def test_model_diagrams_match_validated_candidates(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests/data_profiles") as folder:
            for name in COMPLETE:
                model = parse_validated(ROOT / f"output/data_profiles/{name}.resume")
                for suffix, writer in (("dot", write_tree_dot), ("svg", write_tree_svg)):
                    regenerated = Path(folder) / f"tree.{suffix}"
                    writer(model_tree(model), regenerated)
                    saved = ROOT / f"docs/data_profiles/diagrams/{name}_tree.{suffix}"
                    self.assertEqual(saved.read_bytes(), regenerated.read_bytes())
                tree = ET.parse(ROOT / f"docs/data_profiles/diagrams/{name}_tree.svg")
                labels = [item.text for item in tree.iter() if item.tag.endswith("}text")]
                self.assertIn("name: " + model.personal.name, labels)
                self.assertTrue(all(item.label in labels for item in model.classifications))


if __name__ == "__main__":
    unittest.main()
