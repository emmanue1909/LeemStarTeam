# Empezar por aquí

Abre `examples/resume_01.resume`. Cada registro empieza por una palabra clave: name, email, position, institution, skill, qualification o classification. Experience, Education, Skill, Qualification y Classification se repiten escribiendo otra vez sus palabras clave; mínimo una de cada tipo.

Las clasificaciones van sin comillas. La gramática actual admite Machine Learning Engineer, Data Architect, Full Stack Developer y Cybersecurity Specialist, más Software Architect para compatibilidad histórica. Los clasificadores implementados aquí son únicamente los dos perfiles de datos.

```text
python -m src.stage4.parser examples/resume_01.resume
python -m src.stage4.validator examples/resume_01.resume
python -m src.stage4.markdown_generator examples/resume_01.resume
python -m unittest discover -s tests/tests_stage4 -v
python build_examples.py
```

Parser: sintaxis. Validador: sintaxis y negocio. Generador Markdown: también exige ambas antes de exportar.

La definición está en [Grammar.md](Grammar.md), [Metamodel.md](Metamodel.md) y [validacion.md](validacion.md). Para las cuatro etapas de nuestros perfiles y la interfaz web, inicia en [la guía de perfiles](../data_profiles/README.md).
