# Validación

Entorno: Python 3.12, textX 4.3.0, Arpeggio 2.0.3.

Dos capas de validación, ambas de Emmanuel (`grammar/resume.tx`, `src/validator.py`): la gramática rechaza lo que no calza estructuralmente; el validador aplica las reglas de negocio (años 0-60, nivel 1-5, email con `@` y dominio, teléfono con `+`, sin calificaciones/habilidades repetidas, campos de texto no vacíos).

`tests/valid/` — los 3 ejemplos de `examples/` más el `valid_resume.resume` de Emmanuel. Todos pasan ambas capas.

`tests/invalid/` — un archivo por tipo de error:

| Archivo | Capa que lo rechaza | Error |
|---|---|---|
| `missing_mandatory_field.resume` | gramática | falta `email` |
| `wrong_keyword.resume` | gramática | `year` en vez de `years` |
| `malformed_field.resume` | gramática | `years veinte` (no es INT) |
| `wrong_order.resume` | gramática | `classification` antes de los datos personales |
| `bad_repetition.resume` | gramática | dos valores de `skill` sin repetir la palabra clave |
| `incomplete_profile.resume` | gramática | falta `qualification` y `classification` |
| `semantic_bad_phone.resume` | validador | teléfono sin `+` (sintaxis correcta, regla de negocio no) |

## Reproducir

```bash
python -m unittest tests.test_dsl -v
python build_examples.py
```

`tests/test_dsl.py` corre `src/validator.py` contra cada archivo (que ya incluye el parseo): `tests/valid/*.resume` debe aceptarse sin errores, `tests/invalid/*.resume` debe fallar en la gramática o en alguna regla de negocio.
