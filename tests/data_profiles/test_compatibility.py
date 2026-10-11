import itertools
import unittest

from src.data_app import analyze_text
from src.data_profiles import PROFILES
from src.data_pipeline import evaluate_profiles, run_pipeline, candidate_documents
from src.stage1.extract_data import extract
from src.stage2.normalize_data import normalize_skills
from src.stage3.classify_data import AUTOMATA, EMMANUEL_AUTOMATA, LEGACY_SYMBOLS, classify
from src.data_dsl.validator import mm, validate

COMMON = '''Mi nombre es Ana Pérez.
Radicada en Cali, Colombia.
Email: ana.perez@example.com
Mi posición es Engineer en la compañía Andes. Mi experiencia es de 3 años.
Egresada del programa de Sistemas de la Universidad Icesi; teléfono institucional +57-2-5551234.
Tengo un nivel 4 en Version Control.
'''
FULLSTACK = 'React.js, NodeJS, Postgres, RESTful   API, Git'
CYBER = 'Burp Suite, Pentest, AWS Security, Git'
ML = 'Python, Pandas, sklearn, SQL, Git'
DA = 'Data Modeling, Snowflake, Airflow, AWS, Python, SQL, Git'

class CompatibilityTests(unittest.TestCase):
    def test_shared_common_fields_and_contract_for_all_profiles(self):
        results = evaluate_profiles(COMMON + 'Skills: ' + FULLSTACK + ', ' + CYBER + ', ' + ML + ', ' + DA)
        self.assertEqual(len(results), 4)
        first = results['machine_learning']['extracted']
        self.assertEqual(first['name'], 'Ana Pérez')
        self.assertEqual(first['experiences'], [{'position': 'Engineer', 'company': 'Andes', 'years': 3}])
        for result in results.values():
            self.assertEqual(result['extracted'], first)
            self.assertEqual(result['contract_version'], 3)
            self.assertTrue(result['accepted'])
        model = mm.model_from_str(candidate_documents(results)[0])
        self.assertEqual(validate(model), [])
        self.assertEqual(len(model.classifications), 4)
        self.assertEqual([(q.name, q.level) for q in model.qualifications], [('VERSION_CONTROL', 4)])
        self.assertIn('POSTGRESQL', [s.name for s in model.skills])
        self.assertNotIn('PYTHON', [q.name for q in model.qualifications])

    def test_both_name_and_experience_formats_are_supported(self):
        anchored = extract(COMMON, 'machine_learning')
        old = COMMON.replace('Mi nombre es Ana Pérez.', 'Ana Pérez').replace(
            'Andes. Mi experiencia es de 3 años.', 'Andes; tengo 3 años de experiencia.')
        converted = extract(old, 'machine_learning')
        for field in ('name', 'email', 'location', 'github', 'experiences', 'educations'):
            self.assertEqual(converted[field], anchored[field])

    def test_multiple_emmanuel_experiences_keep_their_own_years(self):
        text = COMMON + '\nMi posición es Analyst en la compañía Otra. Mi experiencia es de 1 año.'
        records = extract(text, 'full_stack')['experiences']
        self.assertEqual([item['years'] for item in records], [3, 1])
        self.assertEqual([item['company'] for item in records], ['Andes', 'Otra'])

    def test_longest_alias_avoids_javascript_from_react_js(self):
        result = run_pipeline('React.js, JS, JavaScript, Postgres, PostgreSQL, RESTful   API', 'full_stack')
        self.assertEqual(result['skills'], ['REACT', 'JAVASCRIPT', 'POSTGRESQL', 'REST_API'])
        self.assertEqual(run_pipeline('React.js', 'full_stack')['skills'], ['REACT'])

    def test_certificates_are_optional_and_do_not_break_cyber(self):
        self.assertTrue(run_pipeline(CYBER, 'cybersecurity')['accepted'])
        self.assertTrue(run_pipeline(CYBER + ', OSCP, Security+', 'cybersecurity')['accepted'])
        self.assertFalse(run_pipeline('CEH, OSCP, Git', 'cybersecurity')['accepted'])

    def test_competence_area_does_not_invent_a_technology(self):
        result = run_pipeline('Tengo un nivel 4 en Data Modeling.', 'data_architect')
        self.assertEqual(result['skills'], [])
        self.assertEqual(result['qualifications'], [{'name': 'DATA_MODELING', 'level': 4}])

    def test_technology_level_does_not_invent_an_area_level(self):
        text = COMMON.replace('Tengo un nivel 4 en Version Control.', '') + 'Skills: ' + ML + ' (nivel 4)'
        report, documents = analyze_text(text, 'machine_learning')
        self.assertTrue(report['profiles']['machine_learning']['accepted'])
        self.assertEqual(report['export_status'], 'BLOCKED')
        self.assertIsNone(documents)

    def test_emmanuel_adapter_preserves_all_representative_subsets(self):
        for profile, original in EMMANUEL_AUTOMATA.items():
            representatives = [tokens[0] for _, tokens in PROFILES[profile]['categories']]
            for count in range(len(representatives) + 1):
                for tokens in itertools.combinations(representatives, count):
                    for order in itertools.permutations(tokens):
                        legacy = [LEGACY_SYMBOLS.get(token, token) for token in order]
                        self.assertEqual(classify(list(order), profile)['accepted'], original.accepts(legacy))

    def test_each_required_category_remains_required_in_every_profile(self):
        for profile, spec in PROFILES.items():
            tokens = [alternatives[0] for _, alternatives in spec['categories']]
            self.assertTrue(classify(tokens, profile)['accepted'])
            for token in tokens:
                result = classify([t for t in tokens if t != token], profile)
                self.assertFalse(result['accepted'])
                self.assertEqual(len(result['missing_categories']), 1)

    def test_extra_known_skills_preserved_without_affecting_recognition(self):
        result = run_pipeline(COMMON + 'Skills: ' + ML + ', Nmap, Security+', 'machine_learning')
        self.assertTrue(result['accepted'])
        self.assertIn('NMAP', result['skills'])
        self.assertNotIn('NMAP', result['classification_input'])

    def test_duplicate_and_conflicting_area_levels(self):
        repeated = COMMON + 'Tengo un nivel 4 en Control de versiones. Skills: ' + ML
        result = run_pipeline(repeated, 'machine_learning')
        self.assertEqual(len(result['qualifications']), 1)
        self.assertEqual(result['qualification_errors'], [])
        bad = repeated + 'Tengo un nivel 2 en Version Control.'
        self.assertIn('Conflicting', run_pipeline(bad, 'machine_learning')['qualification_errors'][0])

    def test_year_boundaries_follow_the_published_team_policy(self):
        for years in (0, 1, 59, 60, 61):
            text = COMMON.replace('3 años', f'{years} años') + 'Skills: ' + ML
            report, _ = analyze_text(text, 'machine_learning')
            self.assertEqual(report['export_status'], 'VALID' if 1 <= years <= 59 else 'BLOCKED')

    def test_canonical_database_policy_is_identical_for_all_profiles(self):
        self.assertEqual(normalize_skills(['Postgres', 'PostgreSQL', 'mySQL'])[0], ['POSTGRESQL', 'MYSQL'])
        for profile in PROFILES:
            self.assertEqual(run_pipeline('Postgres, mySQL', profile)['skills'], ['POSTGRESQL', 'MYSQL'])

    def test_none_one_and_multiple_profiles(self):
        for skills, accepted in [('Git', 0), (ML, 1), (ML + ', ' + FULLSTACK, 2)]:
            results = evaluate_profiles(COMMON + 'Skills: ' + skills)
            self.assertEqual(sum(result['accepted'] for result in results.values()), accepted)
            if accepted:
                model = mm.model_from_str(candidate_documents(results)[0])
                self.assertEqual(len(model.classifications), accepted)

    def test_all_adapted_models_are_deterministic(self):
        self.assertTrue(all(dfa.is_deterministic() for dfa in AUTOMATA.values()))

if __name__ == '__main__':
    unittest.main()
