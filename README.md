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
# LeemStarTeam
Repositorio dedicado a la integradora de discretas 3, relacionada a el filtro de cv's


## Integrated four-profile entry point

The integrated application uses the published Full Stack and Cybersecurity models
from Emmanuel's revision `4a102a7`, together with Machine Learning and Data Architect.
The original contributor modules remain under `src/stage1` through `src/stage4`.
The compatibility layer and data-profile modules provide the combined workflow.

```powershell
python -m pip install -r requirements.txt
python -m src.data_app examples/data_profiles/all_four.pdf --output-dir output/demo
python -m streamlit run src/data_web.py
python run_local.py tests
```

Text-based PDF and UTF-8 text are supported. Scanned PDFs require OCR outside this
application. The combined flow validates the four-profile DSL and the team bounds
of 1..59 years and qualification levels 1..5 before generating Markdown.

The earlier standalone DSL remains available under `src/data_dsl` for historical
examples; its extra Software Architect label is not an integrated fifth classifier.
Use `python -m src.candidate_validation output/data_profiles/all_four.resume` to
validate the current combined output. See [integration](docs/integration.md) and
[shared models](docs/data_profiles/shared_models.md).
