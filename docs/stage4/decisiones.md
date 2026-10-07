# Decisiones — Follow-up 3

Base: la gramática y el validador de Emmanuel (`grammar/resume.tx`, `src/validator.py`, `Grammar.md`, `Metamodel.md`), tal como quedaron en `dev`. Incluyen los 4 perfiles aceptados actuales (Machine Learning Engineer, Full Stack Developer, Cybersecurity Specialist, Software Architect) y `classification` repetible (0 o más perfiles aceptados por candidato, como permite el enunciado).

Nota: el 22-sep el equipo había elegido DevOps Engineer y Data Engineer como los dos perfiles adicionales (ver historial del repo de la Integradora); la gramática actual usa Cybersecurity Specialist y Software Architect en su lugar. Se sigue lo que ya está en `dev`.

## Nuestra parte

`src/markdown_generator.py`, `src/diagram_generator.py` (diagrama de árbol por ejemplo), `build_examples.py`, los 3 ejemplos de `examples/`, y `tests/valid/`+`tests/invalid/`+`tests/test_dsl.py` — 7 casos inválidos: 6 de gramática (uno por cada tipo que pide el enunciado) y 1 de regla de negocio, para cubrir las dos capas de validación.

No se duplicó `Grammar.md`/`Metamodel.md`: ya existen y están al día en `doc/resumelens-dls/`.

## Pendiente

Confirmar equipo/sección y crear el repositorio privado oficial.
