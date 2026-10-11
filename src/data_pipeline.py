import argparse
import json
from pathlib import Path

from src.data_profiles import PROFILES, vocabulary
from src.stage1.extract_data import extract
from src.stage2.normalize_data import canonical_order, normalize_skills, normalize_qualifications
from src.stage3.classify_data import classify
from src.data_dsl.markdown_generator import render_markdown
from src.candidate_validation import parse_candidate
from src.emmanuel_bridge import ASSEMBLER, assembler_input, normalized_profile as team_normalize


def run_pipeline(text, profile, normalized_profile=None):
    extracted = extract(text, profile)
    canonical, unknown = normalize_skills(extracted['raw_skills'])
    declarations = [(item['level'], item['term']) for item in extracted['raw_qualifications']]
    if normalized_profile is None and profile in ('full_stack', 'cybersecurity'):
        normalized_profile = team_normalize(text, profile)
    if normalized_profile is not None:
        # A contributor's result is already normalized; retain only skills
        # supported by raw evidence, including grouped SQL/NOSQL equivalents.
        from src.stage3.classify_data import LEGACY_SYMBOLS
        from src.stage2.normalize_data import translate_one, SKILL_TRANSDUCER
        if not isinstance(normalized_profile, dict) or not all(
                isinstance(normalized_profile.get(key), (list, tuple)) for key in ('skills', 'qualifications')):
            raise ValueError('The team normalizer must return skills and qualifications lists.')
        if not all(isinstance(value, str) for value in normalized_profile['skills']):
            raise ValueError('Team skills must be strings.')
        supplied = set(normalized_profile['skills'])
        known = set(LEGACY_SYMBOLS.get(token, token) for token in canonical)
        for value in supplied:
            token = translate_one(value, SKILL_TRANSDUCER)
            if token is None:
                unknown.append(value)
            elif LEGACY_SYMBOLS.get(token, token) not in known:
                unknown.append(value)
        # Keep explicitly extracted additional area syntax as an extension;
        # identical team/own declarations are deduplicated by the area FST.
        declarations = [*declarations, *normalized_profile['qualifications']]
    qualifications, errors = normalize_qualifications(declarations)
    applicable = [token for token in canonical if token in vocabulary(profile)]
    ordered = canonical_order(applicable, profile)
    return {
        'contract_version': 3,
        "profile": PROFILES[profile]["label"],
        "extracted": extracted,
        'skills': canonical,
        'classification_input': ordered,
        'qualifications': qualifications,
        'qualification_errors': errors,
        "unrecognized": unknown,
        **classify(ordered, profile),
    }


def to_dsl(result, profile):
    if result["profile"] != PROFILES[profile]["label"]:
        raise ValueError("The result and selected profile do not match.")
    if not result["accepted"]:
        raise ValueError("A rejected candidate has no accepted classification to export.")
    data = result["extracted"]
    for field in ("name", "location", "email", "experiences", "educations"):
        if not data[field]:
            raise ValueError(f"Missing candidate information: {field}")
    if result['qualification_errors']:
        raise ValueError('; '.join(result['qualification_errors']))
    if not result['qualifications']:
        raise ValueError('Missing declared qualifications: declare at least one competence area with its level.')
    for job in data["experiences"]:
        if not 1 <= job["years"] <= 59:
            raise ValueError("Experience years outside 1..59 (published team policy)")
    return ASSEMBLER.construir_resume_dsl(assembler_input(
        data, result['skills'], result['qualifications'], [result['profile']]))


def evaluate_profiles(text):
    return {profile: run_pipeline(text, profile) for profile in PROFILES}


def candidate_documents(results):
    accepted = [(profile, result) for profile, result in results.items() if result["accepted"]]
    if not accepted:
        raise ValueError("No accepted profile to export.")
    fields = ("name", "location", "email", "github", "experiences", "educations")
    candidate = accepted[0][1]["extracted"]
    if any(result["extracted"][field] != candidate[field] for _, result in accepted for field in fields):
        raise ValueError("Cannot combine different candidates in one profile.")
    documents = [to_dsl(result, profile) for profile, result in accepted]
    lines = documents[0].splitlines()
    base = [line for line in lines if not line.startswith(("skill ", "qualification ", "classification "))]
    for prefix in ("skill ", "qualification ", "classification "):
        base += list(dict.fromkeys(line for document in documents for line in document.splitlines()
                                  if line.startswith(prefix)))
    dsl = "\n".join(base) + "\n"
    model = parse_candidate(dsl)
    return dsl, render_markdown(model)


def main():
    parser = argparse.ArgumentParser(description='Run the shared pipeline for any of the four profiles')
    parser.add_argument("resume", type=Path)
    parser.add_argument("--profile", choices=PROFILES, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_pipeline(args.resume.read_text(encoding="utf-8"), args.profile)
    content = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content + "\n", encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
