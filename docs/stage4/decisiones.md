# Decisiones del DSL e integración

La gramática, el parser y la base del validador son aportes de Emmanuel. Luis aporta generación de Markdown/árboles, ejemplos, pruebas y la integración de sus perfiles Machine Learning Engineer y Data Architect. Las correcciones comunes conservan esa atribución.

- Gramática vigente: `src/stage4/grammar/resume.tx`; clases y cardinalidades en [Metamodel.md](Metamodel.md).
- `classifications` es una lista de una o más clasificaciones, no un campo singular ni una lista opcional.
- Data Architect es el perfil actual acordado. Software Architect solo conserva los ejemplos históricos del Follow-up 3.
- Una etiqueta en el DSL no demuestra la existencia de su clasificador. Esta contribución ejecuta únicamente los dos perfiles de Luis.
- Tanto la exportación integrada como el generador Markdown independiente comprueban sintaxis y reglas de negocio antes de mostrar un candidato.
- Las rutas de recursos se resuelven desde el archivo fuente, no desde la carpeta desde la cual se ejecuta Python.

Hay cuatro fixtures válidos y nueve inválidos históricos, además de las pruebas actuales de perfiles, exportación e interfaz. Los ejemplos usan datos ficticios. La integración de los otros dos clasificadores y los entregables conjuntos siguen a cargo del equipo.
