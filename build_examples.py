from pathlib import Path

from textx import metamodel_from_file
from textx.export import model_export

from src.diagram_generator import model_tree, write_tree_svg
from src.markdown_generator import render_markdown

ROOT = Path(__file__).resolve().parent
GRAMMAR_PATH = ROOT / "grammar" / "resume.tx"


def main():
    output = ROOT / "output"
    diagrams = ROOT / "doc" / "resumelens-dls" / "diagrams"
    output.mkdir(exist_ok=True)
    diagrams.mkdir(parents=True, exist_ok=True)
    metamodel = metamodel_from_file(str(GRAMMAR_PATH))
    for path in sorted((ROOT / "examples").glob("*.resume")):
        resume = metamodel.model_from_file(str(path), encoding="utf-8")
        (output / f"{path.stem}.md").write_text(render_markdown(resume), encoding="utf-8")
        model_export(resume, str(diagrams / f"{path.stem}_tree.dot"))
        write_tree_svg(model_tree(resume), diagrams / f"{path.stem}_tree.svg")
        print(f"Generated Markdown and model diagram: {path.name}")


if __name__ == "__main__":
    main()
