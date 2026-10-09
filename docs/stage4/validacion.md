# Validación

Dos capas diferentes: textX comprueba la estructura de `src/stage4/grammar/resume.tx`; `src/stage4/validator.py` comprueba reglas de negocio sobre el modelo generado.

| Regla | Comprobación |
|---|---|
| Texto obligatorio | name, location, email, position, company, institution_name, phone, program y nombres de skill/qualification no vacíos ni solo espacios |
| Experiencia | years entre 0 y 60, inclusive |
| Nivel declarado | level entre 1 y 5, inclusive |
| Correo | contiene @ y un punto en el dominio; comprobación básica, no verificación de existencia |
| Teléfono institucional | empieza por +; no comprueba existencia del número |
| Duplicados | no repetir exactamente una classification, skill o qualification |
| Estructura | orden y palabras clave; tipos STRING/INT; al menos una experiencia, educación, skill, qualification y classification |

El exportador de perfiles además exige evidencia original de cada campo y nivel y rechaza niveles contradictorios de alias equivalentes. No inventa datos ni infiere competencia. Las reglas years 0..60 corresponden al validador existente; cualquier cambio de política debe acordarse con el equipo.

Los cuatro fixtures de `tests/tests_stage4/valid/` deben pasar ambas capas. Los nueve de `invalid/` cubren campos ausentes, palabras clave incorrectas, tipo de campo, orden, repetición incompleta, perfil incompleto, errores de gramática/sintaxis históricos y teléfono semánticamente inválido. Las pruebas nuevas incluyen vacíos y cualificaciones repetidas.

```text
python -m unittest discover -s tests/tests_stage4 -v
python -m unittest discover -s tests/data_profiles -p test_validation.py -v
python -m src.stage4.validator examples/resume_01.resume
python -m src.stage4.markdown_generator examples/resume_01.resume
python build_examples.py
```

`parse_validated` y el CLI Markdown rechazan antes de escribir cuando falla cualquiera de las dos capas. El parser aislado solo comprueba sintaxis; no debe confundirse con una exportación validada.
