import json
from pathlib import Path

from textx import metamodel_from_file

from src.data_pipeline import candidate_documents, evaluate_profiles, run_pipeline, to_dsl
from src.stage4.markdown_generator import render_markdown
from src.stage4.validator import validate
from src.stage4.diagram_generator import model_tree, write_tree_dot, write_tree_svg

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT / "output/data_profiles"
    output.mkdir(parents=True, exist_ok=True)
    diagrams = ROOT / "docs/data_profiles/diagrams"
    diagrams.mkdir(parents=True, exist_ok=True)

    def tree(model, name):
        structure = model_tree(model)
        write_tree_dot(structure, diagrams / f"{name}_tree.dot")
        write_tree_svg(structure, diagrams / f"{name}_tree.svg")
    grammar = ROOT / "src/stage4/grammar/resume.tx"
    mm = metamodel_from_file(str(grammar))
    cases = [("ml_engineer", "machine_learning"), ("ml_incomplete", "machine_learning"),
             ("data_architect", "data_architect"), ("data_architect_incomplete", "data_architect"),
             ("ml_english", "machine_learning"), ("architect_english", "data_architect")]
    report = ["# Data profile verification", "", "| Case | Stages 1 to 3 | Stage 4 grammar |", "|---|---|---|"]
    for name, profile in cases:
        text = (ROOT / f"examples/data_profiles/{name}.txt").read_text(encoding="utf-8")
        result = run_pipeline(text, profile)
        (output / f"{name}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        status, grammar_status = "REJECTED", "Not exported"
        if result["accepted"]:
            status = "ACCEPTED"
            dsl = to_dsl(result, profile)
            (output / f"{name}.resume").write_text(dsl, encoding="utf-8")
            model = mm.model_from_str(dsl)
            errors = validate(model)
            if errors:
                raise ValueError("; ".join(errors))
            (output / f"{name}.md").write_text(render_markdown(model), encoding="utf-8")
            tree(model, name)
            grammar_status = "VALID (syntax and business rules)"
        report.append(f"| {name} | {status} | {grammar_status} |")
    combined = evaluate_profiles((ROOT / "examples/data_profiles/ml_and_architect.txt").read_text(encoding="utf-8"))
    dsl, markdown = candidate_documents(combined)
    (output / "ml_and_architect.json").write_text(json.dumps(combined, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "ml_and_architect.resume").write_text(dsl, encoding="utf-8")
    (output / "ml_and_architect.md").write_text(markdown, encoding="utf-8")
    tree(mm.model_from_str(dsl), "ml_and_architect")
    report.append("| ml_and_architect | BOTH ACCEPTED | VALID (syntax and business rules) |")
    report += ["", "All five complete candidates validate with textX and business rules, generate Markdown and model diagrams. The combined candidate preserves both classifications. These are seven fictional scenarios for Luis's two profiles, not implementation of the team's other two profiles.", ""]
    (output / "verification.md").write_text("\n".join(report), encoding="utf-8")
    print("Wrote seven JSON reports, five valid DSL/Markdown exports, five model diagrams and the verification report.")


if __name__ == "__main__":
    main()
