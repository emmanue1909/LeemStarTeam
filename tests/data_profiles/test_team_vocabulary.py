import itertools
import json
from pathlib import Path
import unittest

from src.data_app import analyze_text
from src.data_profiles import PROFILES
from src.data_pipeline import run_pipeline
from src.stage3.classify_data import LEGACY_SYMBOLS

COMMON = '''Mi nombre es Ana Pérez.
Radicada en Cali, Colombia.
Email: ana.perez@example.com
Mi posición es Engineer en la compañía Andes. Mi experiencia es de 3 años.
Egresada del programa de Sistemas de la Universidad Icesi; teléfono institucional +57-2-5551234.
Tengo un nivel 4 en Version Control.
'''


class TeamVocabularyTests(unittest.TestCase):
    def test_published_emmanuel_aliases_keep_complete_raw_evidence(self):
        # Frozen from the two skill tables at root-emmanuel commit 922c0d2.
        path = Path(__file__).parent / 'fixtures/emmanuel_skill_aliases_922c0d2.json'
        for item in json.loads(path.read_text(encoding='utf-8')):
            with self.subTest(alias=item['alias']):
                result = run_pipeline('Skills: ' + item['alias'], item['profile'])
                self.assertEqual(result['extracted']['raw_skills'], [item['alias']])
                self.assertEqual(result['skills'], [item['canonical']])
                self.assertEqual(LEGACY_SYMBOLS.get(item['canonical'], item['canonical']), item['legacy'])

    def test_long_aliases_complete_full_stack_export(self):
        for frontend in ('Java Script', 'Type Script'):
            report, documents = analyze_text(COMMON + 'Skills: ' + frontend + ', Node, Postgres, REST API, Git', 'full_stack')
            self.assertTrue(report['profiles']['full_stack']['accepted'])
            self.assertEqual(report['export_status'], 'VALID')
            self.assertIn('skill "NODEJS"', documents[0])

    def test_long_security_aliases_complete_cyber_export_without_plain_cloud_claim(self):
        for cloud, canonical in [('Amazon Web Services Security', 'AWS_SECURITY'), ('Microsoft Azure Security', 'AZURE_SECURITY')]:
            text = COMMON + 'Skills: Network Mapper, Open Web Application Security Project, ' + cloud + ', Git'
            report, documents = analyze_text(text, 'cybersecurity')
            result = report['profiles']['cybersecurity']
            self.assertTrue(result['accepted'])
            self.assertEqual(report['export_status'], 'VALID')
            self.assertIn(canonical, result['skills'])
            self.assertNotIn('AWS' if canonical == 'AWS_SECURITY' else 'AZURE', result['skills'])
            self.assertIn('skill "' + canonical + '"', documents[0])

    def test_plain_cloud_and_related_platforms_do_not_satisfy_security_or_git(self):
        self.assertFalse(run_pipeline('Nmap, Pentest, AWS, Azure, Git', 'cybersecurity')['accepted'])
        self.assertFalse(run_pipeline('Nmap, Pentest, AWS Security, GitHub, GitLab', 'cybersecurity')['accepted'])
        self.assertEqual(run_pipeline('Spring, NodeGraph, Burping', 'full_stack')['skills'], [])

    def test_ordered_data_pipeline_matches_category_coverage_on_all_subsets(self):
        for profile in ('machine_learning', 'data_architect'):
            groups = PROFILES[profile]['categories']
            representatives = [alternatives[0] for _, alternatives in groups]
            for count in range(len(representatives) + 1):
                for subset in itertools.combinations(representatives, count):
                    expected = count == len(groups)
                    for order in (subset, tuple(reversed(subset))):
                        with self.subTest(profile=profile, subset=order):
                            # Original résumé order differs; the allowed preparation step sorts.
                            result = run_pipeline('Skills: ' + ', '.join(order + order), profile)
                            self.assertEqual(result['accepted'], expected)


if __name__ == '__main__':
    unittest.main()
