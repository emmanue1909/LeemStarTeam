import argparse
import json
from pathlib import Path

from src.data_profiles import PROFILES
from src.stage1.extract_data import extract
from src.stage2.normalize_data import canonical_order, normalize, normalize_one
from src.stage3.classify_data import classify
from src.stage4.markdown_generator import render_markdown
from src.stage4.validator import mm, validate


def run_pipeline(text, profile):
    extracted = extract(text, profile)
    canonical, unknown = normalize(extracted["raw_qualifications"], profile)
    ordered = canonical_order(canonical, profile)
    return {
        "profile": PROFILES[profile]["label"],
        "extracted": extracted,
        "qualifications": ordered,
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
    levels = {}
    for declaration in data["declared_levels"]:
        token = normalize_one(declaration["term"], profile)
        if token is not None:
            value = declaration["level"]
            if not 1 <= value <= 5:
                raise ValueError(f"Declared level outside 1..5: {token}")
            if token in levels and levels[token] != value:
                raise ValueError(f"Conflicting declared levels: {token}")
            levels[token] = value
    missing = set(result["qualifications"]) - levels.keys()
    if missing:
        raise ValueError("Missing declared levels: " + ", ".join(sorted(missing)))
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    lines = [f'name {quote(data["name"])} location {quote(data["location"])}', f'email {quote(data["email"])}']
    if data["github"]:
        lines[-1] += f' github {quote(data["github"])}'
    for job in data["experiences"]:
        if not 0 <= job["years"] <= 60:
            raise ValueError("Experience years outside 0..60")
        lines.append(f'position {quote(job["position"])} company {quote(job["company"])} years {job["years"]}')
    for study in data["educations"]:
        lines.append(f'institution {quote(study["institution"])} phone {quote(study["phone"])} program {quote(study["program"])}')
    lines += [f'skill {quote(token)}' for token in result["qualifications"]]
    lines += [f'qualification {quote(token)} level {levels[token]}' for token in result["qualifications"]]
    lines.append(f'classification {result["profile"]}')
    return "\n".join(lines) + "\n"


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
    model = mm.model_from_str(dsl)
    errors = validate(model)
    if errors:
        raise ValueError("Invalid candidate profile: " + "; ".join(errors))
    return dsl, render_markdown(model)


def main():
    parser = argparse.ArgumentParser(description="Run the shared pipeline for ML and Data Architect profiles")
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
