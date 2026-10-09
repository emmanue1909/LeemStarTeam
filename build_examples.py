from pathlib import Path

from textx.export import model_export

from src.stage4.diagram_generator import model_tree, write_tree_svg
from src.stage4.markdown_generator import render_markdown
from src.stage4.validator import parse_validated

ROOT = Path(__file__).resolve().parent


def main():
    output = ROOT / "output"
    diagrams = ROOT / "docs" / "stage4" / "diagrams"
    output.mkdir(exist_ok=True)
    diagrams.mkdir(parents=True, exist_ok=True)
    for path in sorted((ROOT / "examples").glob("*.resume")):
        resume = parse_validated(path)
        (output / f"{path.stem}.md").write_text(render_markdown(resume), encoding="utf-8")
        model_export(resume, str(diagrams / f"{path.stem}_tree.dot"))
        write_tree_svg(model_tree(resume), diagrams / f"{path.stem}_tree.svg")
        print(f"Generated Markdown and model diagram: {path.name}")


if __name__ == "__main__":
    main()
