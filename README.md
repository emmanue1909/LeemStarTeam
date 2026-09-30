# resumelens-dsl--team-emmanuel-

Repositorio creado para trabajar un DSL para CVs donde se logre hacer filtro, aceptando o rechazando CVs en base a ciertas características. DSL de ResumeLens (Follow-up 3, CyED III): representa el perfil de un candidato — datos personales, experiencia, educación, habilidades, calificaciones normalizadas y el resultado de su clasificación — validado con textX.

## Equipo

- Emmanuel — GitHub: `emmanue1909` — gramática (`grammar/resume.tx`), validador de reglas de negocio (`src/validator.py`), parser (`src/parser.py`), documentación EBNF y de metamodelo.
- Luis Eduardo Grijalba Franco — GitHub: `luiseduardogf` — generador de Markdown, diagramas de árbol por ejemplo, ejemplos, tests.

## Requisitos

```bash
python -m pip install -r requirements.txt
```

## Uso

```bash
python src/parser.py examples/resume_01.resume
python src/validator.py examples/resume_01.resume
python src/markdown_generator.py examples/resume_01.resume
python build_examples.py
python -m unittest tests.test_dsl -v
```

## Estructura

| Ruta | Contenido |
|---|---|
| `grammar/resume.tx` | Gramática textX |
| `src/parser.py`, `src/validator.py` | Aceptación sintáctica y reglas de negocio |
| `src/markdown_generator.py`, `src/diagram_generator.py` | Visualización Markdown y diagramas de árbol |
| `examples/` | 3 currículos de ejemplo |
| `output/`, `doc/resumelens-dls/diagrams/` | Markdown y diagramas generados |
| `doc/resumelens-dls/` | Documentación (gramática, metamodelo, validación, registro de IA) |
| `tests/` | Casos válidos e inválidos |

Ver `doc/resumelens-dls/Empezar_aqui.md` para una primera lectura.
