import argparse
from pathlib import Path
from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError

GRAMMAR_PATH = Path(__file__).resolve().parent / "grammar/resume.tx"


def main():
    parser = argparse.ArgumentParser(description="Validate ResumeLens syntax")
    parser.add_argument("resume", type=Path)
    args = parser.parse_args()
    try:
        metamodel_from_file(str(GRAMMAR_PATH)).model_from_file(str(args.resume), encoding="utf-8")
    except TextXSyntaxError as error:
        parser.exit(1, f"Error de sintaxis: {error}\n")
    print("Modelo aceptado")


if __name__ == "__main__":
    main()
