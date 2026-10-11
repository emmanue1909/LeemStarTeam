"""Our compatibility layer around unchanged contributor modules at 4a102a7."""
import importlib.util
from pathlib import Path
import sys
from types import ModuleType

SNAPSHOT = Path(__file__).resolve().parent / 'vendor/emmanuel_4a102a7/src'


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, SNAPSHOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CLASSIFIER = load_module('resumelens_team_classifier', 'stage3/classification.py')
ASSEMBLER = load_module('resumelens_team_assembler', 'stage4/assembler.py')
VALIDATOR = load_module('resumelens_team_validator', 'stage4/validator.py')
SPECIFIC = load_module('resumelens_team_extractor', 'stage1/extract_specific.py')

# The contributor imports `stage1` as a top-level package. Supply that binding
# while loading his module, then restore the caller's module namespace.
package = ModuleType('stage1')
package.extract_specific = SPECIFIC
previous = sys.modules.get('stage1')
try:
    sys.modules['stage1'] = package
    NORMALIZER = load_module('resumelens_team_normalizer', 'stage2/normalization.py')
finally:
    if previous is None:
        sys.modules.pop('stage1', None)
    else:
        sys.modules['stage1'] = previous


def normalized_profile(text, profile):
    functions = {'full_stack': NORMALIZER.normalizar_perfil_fullstack,
                 'cybersecurity': NORMALIZER.normalizar_perfil_cyber}
    return functions[profile](text)


def assembler_input(data, skills, qualifications, labels):
    return {
        'nombre': data['name'], 'ubicacion': data['location'],
        'email': data['email'], 'github': data['github'],
        'experiencias': [{'position': job['position'], 'company': job['company'],
                          'years': job['years']} for job in data['experiences']],
        'educaciones': [{'institucion': study['institution'], 'phone': study['phone'],
                         'program': study['program']} for study in data['educations']],
        'skills': skills, 'qualifications': [(item['level'], item['name']) for item in qualifications],
        'clasificaciones_aceptadas': labels,
    }
