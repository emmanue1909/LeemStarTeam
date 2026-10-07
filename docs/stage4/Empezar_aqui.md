# Empezar por aquí

Abre `examples/resume_01.resume`. No hay llaves ni corchetes: cada línea empieza con una palabra clave que marca la sección (`name`, `email`, `position`, `institution`, `skill`, `qualification`, `classification`). Las secciones repetibles (`position`, `institution`, `skill`, `qualification`, `classification`) se repiten escribiendo la palabra clave de nuevo, sin separador — mínimo una vez cada una.

`classification` acepta uno de cuatro valores fijos, **sin comillas** (`Machine Learning Engineer`, `Full Stack Developer`, `Cybersecurity Specialist`, `Software Architect`), y se puede repetir para un candidato con varios perfiles aceptados — ver `resume_03.resume`.

Hay dos niveles de validación: `src/parser.py` (gramática) y `src/validator.py` (reglas de negocio: años, niveles, formato de correo/teléfono, sin duplicados). Un archivo puede pasar el parser y aun así ser rechazado por el validador.

```bash
python -m unittest tests.test_dsl -v
python build_examples.py
python src/parser.py examples/resume_01.resume
python src/validator.py examples/resume_01.resume
python src/markdown_generator.py examples/resume_01.resume
```

Ver `doc/resumelens-dls/Grammar.md` y `Metamodel.md` (Emmanuel) para la definición formal, y `validacion.md` para el detalle de qué prueba cada test.
