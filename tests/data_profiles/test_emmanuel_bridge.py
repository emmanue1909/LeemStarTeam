import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from src.data_app import analyze_text
from src.data_pipeline import run_pipeline, candidate_documents
from src.emmanuel_bridge import ASSEMBLER, VALIDATOR, normalized_profile
from src.stage2.normalize_data import normalize_qualifications
from src.stage3.classify_data import AUTOMATA, EMMANUEL_AUTOMATA, state_coverage
from src.candidate_validation import parse_candidate

ROOT = Path(__file__).resolve().parents[2]
COMMON = '''Mi nombre es Ana Perez.
Radicada en Cali, Colombia.
Email: ana.perez@example.com
Mi posición es Engineer en la compañía Andes. Mi experiencia es de 3 años.
Egresada del programa de Sistemas de la Universidad Icesi; teléfono institucional +57-2-5551234.
Tengo un nivel 4 en Version Control.
'''


class EmmanuelBridgeTests(unittest.TestCase):
    def test_contributor_snapshot_is_byte_identical_to_its_manifest(self):
        folder = ROOT / 'src/vendor/emmanuel_4a102a7'
        manifest = json.loads((folder / 'SOURCE.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['revision'], '4a102a73e4c04cacda5ae24f9324ce4250a0f058')
        for relative, expected in manifest['files'].items():
            self.assertEqual(hashlib.sha256((folder / relative).read_bytes()).hexdigest(), expected)

    def test_qualifications_consume_actual_team_tuple_shape_and_string_levels(self):
        text = COMMON + 'Skills: React, NodeJS, Postgres, REST API, Git'
        payload = normalized_profile(text, 'full_stack')
        self.assertIn(('4', 'VERSION CONTROL'), payload['qualifications'])
        result = run_pipeline(text, 'full_stack', normalized_profile=payload)
        self.assertTrue(result['accepted'])
        self.assertEqual(result['qualifications'], [{'name': 'VERSION_CONTROL', 'level': 4}])
        dsl, markdown = candidate_documents({'full_stack': result})
        self.assertEqual(VALIDATOR.validate(VALIDATOR.mm.model_from_str(dsl)), [])
        self.assertIn('Full Stack Developer', markdown)

    def test_default_pipeline_calls_the_published_normalizer(self):
        from src.data_pipeline import team_normalize
        with patch('src.data_pipeline.team_normalize', wraps=team_normalize) as call:
            report, _ = analyze_text(COMMON + 'Skills: Nmap, Pentest, AWS Security, Git', 'cybersecurity')
            call.assert_called_once()
            self.assertEqual(report['export_status'], 'VALID')

    def test_assembler_consumes_the_contributor_contract(self):
        with patch.object(ASSEMBLER, 'construir_resume_dsl', wraps=ASSEMBLER.construir_resume_dsl) as call:
            report, _ = analyze_text(COMMON + 'Skills: Python, Pandas, sklearn, SQL, Git', 'machine_learning')
            self.assertEqual(report['export_status'], 'VALID')
            payload = call.call_args.args[0]
            self.assertEqual(payload['qualifications'], [(4, 'VERSION_CONTROL')])
            self.assertEqual(payload['experiencias'][0]['years'], 3)
            self.assertEqual(payload['educaciones'][0]['institucion'], 'Universidad Icesi')

    def test_no_contributor_state_is_renamed(self):
        for profile, original in EMMANUEL_AUTOMATA.items():
            adapted = AUTOMATA[profile]
            self.assertEqual(original.states, adapted.states)
            self.assertEqual(original.final_states, adapted.final_states)
            self.assertEqual(len(state_coverage(profile)), len(original.states))

    def test_tuple_duplicates_conflicts_and_invalid_levels_remain_checked(self):
        self.assertEqual(normalize_qualifications([('4', 'VERSION CONTROL'), (4, 'VERSION_CONTROL')]),
                         ([{'name': 'VERSION_CONTROL', 'level': 4}], []))
        for declarations in [[('4', 'VERSION CONTROL'), (2, 'VERSION CONTROL')],
                             [('9', 'VERSION CONTROL')], [('unknown', 'VERSION CONTROL')], [None]]:
            self.assertTrue(normalize_qualifications(declarations)[1])

    def test_quote_backslash_and_newline_survive_the_original_assembler(self):
        result = run_pipeline(COMMON + 'Skills: Python, Pandas, sklearn, SQL, Git', 'machine_learning')
        company = 'Andes "Lab" \\ Systems\nSecond line'
        result['extracted']['experiences'][0]['company'] = company
        dsl, _ = candidate_documents({'machine_learning': result})
        model = VALIDATOR.mm.model_from_str(dsl)
        self.assertEqual(model.experiences[0].company, company)

    def test_integrated_validator_applies_team_bounds_to_manually_edited_dsl(self):
        result = run_pipeline(COMMON + 'Skills: Python, Pandas, sklearn, SQL, Git', 'machine_learning')
        dsl, _ = candidate_documents({'machine_learning': result})
        for years in (0, 60):
            with self.assertRaisesRegex(ValueError, 'outside 1..59'):
                parse_candidate(dsl.replace('years 3', 'years ' + str(years)))


if __name__ == '__main__':
    unittest.main()
