## Objetivo 
Normalizar las variantes de skills y qualifications que la Etapa 1 extrajo en crudo (ej. "mySQL", "JS", "Pentest") a su forma canónica única (ej. "SQL", "JavaScript", "Penetration Testing"), para que la Etapa 3 pueda clasificar contra una lista cerrada y consistente. 
## Alcance 
Solo se normalizan skills y qualifications. Los 8 campos comunes (email, teléfono, nombre, etc.) ya salen en su forma final desde la Etapa 1 y no pasan por este transductor. 
## Definición formal
Se modela cada skill/qualification como un transductor de estados finitos independiente, mediante la 7-tupla (Q, Σ, Γ, δ, σ, q₀, F): 
- **Q** = {q0, qf}  dos estados: el estado inicial y el estado de aceptación. 
- **Σ** = conjunto de variantes reconocidas para esa skill/qualification (alfabeto de entrada). Ej. para SQL: {SQL, MySQL, PostgreSQL, Postgres}. 
- **Γ** = {nombre canónico} alfabeto de salida, un único símbolo (ej. {SQL}). 
- **δ** = función de transición: δ(q₀, variante) = qf, para toda variante ∈ Σ. 
- **σ** = función de salida: σ(q₀, variante) = nombre canónico, para toda variante ∈ Σ. 
- **F** = {qf}. 
En otras palabras: cada transductor recibe como entrada completa una de las variantes reconocidas (el texto crudo que extrajo Stage 1) y, en una sola transición, produce el nombre canónico correspondiente. No hay estados intermedios porque la variante se consume como un único símbolo atómico (la palabra completa), no caracter por caracter. 
## Mapas de normalización 
Las tablas canónico → variantes de cada skill/qualification ya están documentadas en `docs/stage1_regex/formalizacion.md`, sección "Abreviaciones y variantes reconocidas". Stage 2 reutiliza esas mismas tablas (invertidas a canónico → [variantes]) para construir los transductores, así que no se duplican aquí. 

**Nota:** sobre qualifications Las qualifications no tienen variantes reconocidas (se extraen ya con el nombre completo, por decisión de Stage 1), por lo que su transductor es trivial: Σ = {nombre completo} = Γ, es decir, δ y σ mapean la única entrada a sí misma. Se modelan igual con la 7-tupla por consistencia formal con las skills, aunque en la práctica no normalizan nada.