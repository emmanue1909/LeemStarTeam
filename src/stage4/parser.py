import sys
from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError

#metamodel
mm = metamodel_from_file("grammar/resume.tx")

if len(sys.argv) != 2:
        print("Uso: python src/parser.py <archivo.resume>")
        sys.exit(1)

file_path = sys.argv[1]

try:
    model = mm.model_from_file(file_path)
    print("modelo aceptado")
except TextXSyntaxError as e:
    print(f"Error de sintaxis en {file_path}: {e}")
