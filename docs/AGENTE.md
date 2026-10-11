# Guía y Directiva de Agentes de IA (`AGENTE.md`)

Este archivo define el contexto del proyecto y establece las **reglas obligatorias e inmutables** que cualquier agente de inteligencia artificial (o asistente de desarrollo) debe cumplir estrictamente al operar dentro de este repositorio.

---

## ⚠️ DIRECTIVA PRINCIPAL PARA AGENTES (REGLA INQUEBRANTABLE)

> [!IMPORTANT]
> **ALCANCE EXCLUSIVO DE LOS AGENTES EN ESTE REPOSITORIO**
>
> **La ÚNICA función autorizada para los agentes en este proyecto es cambiar el idioma de los documentos (traducir de español a inglés los documentos que el usuario solicite explícitamente en el prompt).**

### Restricciones y Prohibiciones Estrictas:
1. **Traducción bajo demanda explícita:** El agente solo traducirá los archivos o documentos que el usuario mencione y solicite explícitamente en el prompt. No debe traducir ni alterar archivos de forma proactiva o no solicitada.
2. **Prohibido tocar lógica de código:** Ningún agente tiene permitido modificar, refactorizar, optimizar, añadir o eliminar código fuente en `src/`, definiciones de gramática en `grammar/`, scripts de construcción como `build_examples.py`, ni casos de prueba en `tests/`.
3. **Prohibido alterar la información o el contenido:** La traducción debe ser **estricta, fiel y directa**. No se permite cambiar el sentido, eliminar conceptos, resumir, expandir, interpretar o alterar datos, decisiones de diseño, algoritmos, explicaciones teóricas ni conclusiones.
4. **Preservación estructural:** Se deben mantener intactos todos los identificadores de código, bloques de código (`code blocks`), enlaces relativos o absolutos, metadatos, fórmulas matemáticas y formato original Markdown.

---

## 📖 Resumen y Especificación del Proyecto

### Contexto General
- **Nombre del Proyecto:** LeemStarTeam / ResumeLens DSL
- **Curso:** Computabilidad y Estructuras Discretas III (CyED III) - Universidad Icesi
- **Propósito:** Proyecto integrador dedicado al procesamiento formal, extracción, normalización, clasificación y validación de hojas de vida (CVs) técnicas de candidatos mediante teoría de autómatas, lenguajes formales y desarrollo de lenguajes de dominio específico (DSL).

---

### Arquitectura por Etapas del Pipeline

El sistema se compone de cuatro etapas secuenciales diseñadas a partir de modelos formales de computación:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Etapa 1    │ ──> │   Etapa 2    │ ──> │   Etapa 3    │ ──> │   Etapa 4    │
│    Regex     │     │     FST      │     │  Autómatas   │     │   DSL textX  │
│ (Extracción) │     │(Normalización│     │(Clasificación│     │ (Validación) │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

#### 1. Etapa 1: Extracción con Expresiones Regulares (`docs/satge1/`)
- **Herramienta:** Módulo `re` de Python.
- **Objetivo:** Extraer información cruda del texto no estructurado de las hojas de vida a partir de frases ancla y patrones regex formales.
- **Campos procesados:** Información personal (email, teléfono, nombre, ubicación, perfil de GitHub), educación (programa e institución), experiencia laboral (años, cargo y empresa), y listados crudos de *skills* y *qualifications*.

#### 2. Etapa 2: Normalización con Transductores de Estados Finitos (FST) (`docs/stage2/`)
- **Modelo:** Transductores de Estados Finitos modelados con la 7-tupla formal $(Q, \Sigma, \Gamma, \delta, \sigma, q_0, F)$.
- **Objetivo:** Recibir las variantes léxicas y abreviaciones extraídas en crudo en la Etapa 1 (ej. `"mySQL"`, `"JS"`, `"Pentest"`) y transducirlas a su forma canónica normalizada (ej. `"SQL"`, `"JavaScript"`, `"Penetration Testing"`).
- **Alcance:** Aplica a habilidades (*skills*) y cualificaciones (*qualifications*).

#### 3. Etapa 3: Clasificación con Autómatas Finitos (`docs/stage3/`)
- **Modelo:** Autómatas Finitos Deterministas / No Deterministas (DFA/NFA).
- **Objetivo:** Clasificar los perfiles de los candidatos contra los requisitos formales de las áreas técnicas objetivo (Full Stack Developer, Machine Learning Engineer, Cybersecurity Specialist, Software Architect).
- **Criterio:** Determina si el conjunto de habilidades canónicas del candidato satisface todos los requisitos y categorías obligatorias para cada perfil.

#### 4. Etapa 4: Dominio Específico (DSL textX) y Reglas de Negocio (`docs/stage4/`, `grammar/`, `src/`)
- **Herramienta:** `textX` para Python.
- **Gramática (`grammar/resume.tx`):** Define la sintaxis declarativa del DSL estructurado por palabras clave (`name`, `email`, `position`, `institution`, `skill`, `qualification`, `classification`).
- **Análisis Sintáctico (`src/parser.py`):** Valida la conformidad estructural del archivo `.resume` contra la gramática formal.
- **Validador Semántico (`src/validator.py`):** Aplica validaciones de reglas de negocio que exceden la sintaxis libre de contexto (rango de años de experiencia entre 1 y 59, formato de correo, teléfonos y descarte de duplicados).
- **Generadores (`src/markdown_generator.py`, `src/diagram_generator.py`):** Generan reportes Markdown estandarizados y diagramas de árboles sintácticos en formato Graphviz/SVG.

---

## 📂 Estructura de Directorios del Repositorio

```
LeemStarTeam/
├── docs/                      # Documentación del proyecto por etapas
│   ├── AGENTE.md              # Este archivo: directiva y contexto para IAs
│   ├── satge1/                # Etapa 1: Regex y extracción cruda
│   ├── stage2/                # Etapa 2: FST y normalización canónica
│   ├── stage3/                # Etapa 3: Autómatas y clasificación de perfiles
│   └── stage4/                # Etapa 4: Decisiones, gramática y validación
├── grammar/                   # Definición de la gramática formal textX (.tx)
├── src/                       # Parser, validador de negocio y generadores
├── examples/                  # Ejemplos de hojas de vida (.resume)
├── output/                    # Archivos generados (Markdown y reportes)
├── tests/                     # Pruebas unitarias de sintaxis y validación
├── build_examples.py          # Script de construcción y ejecución de ejemplos
└── requirements.txt           # Dependencias del proyecto
```

---

## 📌 Guía de Traducción para Agentes

Cuando el usuario pida en un prompt: *"Traduce el archivo X de español a inglés"* (o equivalente):

1. **Traducción fiel y técnica:** Traducir los textos explicativos conservando la terminología formal de ciencias de la computación (ej. *Finite State Transducer*, *Context-Free Grammar*, *Canonical Form*, *Transition Function*).
2. **Inmutabilidad de código:** No traducir nombres de variables, nombres de funciones, comandos de terminal (`bash`, `python`), ni nombres de archivos referenciados.
3. **Respeto al formato Markdown:** Mantener encabezados, tablas, listas y bloques de advertencia intactos.
4. **Sin alteraciones adicionales:** No agregar opiniones, cambios en el contenido ni modificaciones fuera de la traducción solicitada.
