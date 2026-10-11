"""Apply the published 1..59 team policy without editing contributor validators."""
import argparse
from pathlib import Path

from src.data_dsl.validator import mm, validate as base_validate
from src.emmanuel_bridge import VALIDATOR


def validate_candidate(model):
    errors = base_validate(model)
    for job in model.experiences:
        if not 1 <= job.years <= 59:
            errors.append('Experience years outside 1..59 (published team policy)')
    return errors


def parse_candidate(text):
    model = mm.model_from_str(text)
    errors = validate_candidate(model)
    errors += VALIDATOR.validate(VALIDATOR.mm.model_from_str(text))
    if errors:
        raise ValueError('Invalid candidate profile: ' + '; '.join(dict.fromkeys(errors)))
    return model


def main():
    parser = argparse.ArgumentParser(description='Validate the integrated candidate DSL')
    parser.add_argument('resume', type=Path)
    args = parser.parse_args()
    parse_candidate(args.resume.read_text(encoding='utf-8'))
    print('VALID')


if __name__ == '__main__':
    main()
