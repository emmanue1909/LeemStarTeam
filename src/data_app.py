import argparse
import json
from pathlib import Path

from textx.exceptions import TextXSyntaxError

from src.data_pipeline import candidate_documents, evaluate_profiles, run_pipeline
from src.data_profiles import PROFILES


def analyze_text(text, profile="all"):
    if not text.strip():
        raise ValueError("Enter résumé text before analyzing.")
    results = evaluate_profiles(text) if profile == "all" else {profile: run_pipeline(text, profile)}
    report = {"profiles": results, "export_status": "NOT_ACCEPTED"}
    documents = None
    if any(result["accepted"] for result in results.values()):
        try:
            documents = candidate_documents(results)
            report["export_status"] = "VALID"
        except (ValueError, TextXSyntaxError) as error:
            report.update(export_status="BLOCKED", export_error=str(error))
    return report, documents


def process_file(source, output, profile="all"):
    source, output = Path(source), Path(output)
    artifacts = [output / name for name in ("report.json", "candidate.resume", "candidate.md")]
    if any(path.exists() for path in artifacts):
        raise ValueError("Choose a new output folder; existing results will not be overwritten.")
    report, documents = analyze_text(source.read_text(encoding="utf-8"), profile)
    report["source"] = source.name
    output.mkdir(parents=True, exist_ok=True)
    artifacts[0].write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if documents:
        for path, content in zip(artifacts[1:], documents):
            path.write_text(content, encoding="utf-8")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description="ResumeLens: evaluate and visualize the two data profiles")
    parser.add_argument("resume", type=Path)
    parser.add_argument("--profile", choices=["all", *PROFILES], default="all")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = process_file(args.resume, args.output_dir, args.profile)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    for result in report["profiles"].values():
        status = "ACCEPTED" if result["accepted"] else "REJECTED"
        print(f'{result["profile"]}: {status}')
        if result["missing_categories"]:
            print("  Missing: " + ", ".join(result["missing_categories"]))
    print("Candidate export: " + report["export_status"])
    if "export_error" in report:
        print("  " + report["export_error"])
    print("Output: " + str(args.output_dir.resolve()))
    return 2 if report["export_status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
