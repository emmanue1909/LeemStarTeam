
## Objetivo 
Clasificar un fragmento de hoja de vida en uno o varios de los perfiles definidos (Full Stack Developer, Cybersecurity Specialist), a partir de los skills ya normalizados por Stage 2. La clasificación se hace con un autómata finito determinista (DFA) independiente por perfil. 
## Alcance 
- Cada perfil tiene su propio DFA; se evalúan de forma independiente. Un candidato puede ser aceptado por ninguno, uno o $n$ perfiles ($p$) donde $0 \leq n \leq p$,  no es excluyente. 
- La entrada de cada DFA es la secuencia de skills normalizados que produjo Stage 2 (no el texto crudo). 
- Un skill que no pertenece a ninguna qualification del perfil evaluado (por ejemplo, un skill de Cybersecurity al evaluar Full Stack, o una certificación opcional como CEH/OSCP/Security+) no hace nada: el autómata se queda en el mismo estado (bucle). 
- El orden en que aparecen los skills no importa para el resultado, el autómata solo acumula cobertura, nunca la pierde. 
## Mapeo: skill $\rightarrow$ qualification 
**Full Stack Developer** 

| Qualification        | Skills que la cubren                        |
| -------------------- | ------------------------------------------- |
| Frontend Development | JavaScript, TypeScript, React, Angular, Vue |
| Backend Development  | Node.js, Django, Spring Boot                |
| Database Management  | SQL, NoSQL                                  |
| API Integration      | APIs REST                                   |
| Version Control      | Git                                         |

**Cybersecurity Specialist** 

| Qualification      | Skills que la cubren                                                    |
| ------------------ | ----------------------------------------------------------------------- |
| Security Tools     | Nmap, Wireshark, Burp Suite, Metasploit                                 |
| Security Practices | Penetration Testing, Vulnerability Assessment, OWASP, Incident Response |
| Cloud Security     | AWS Security, Azure Security                                            |
| Version Control    | Git                                                                     |

CEH, OSCP y Security+ no pertenecen a ninguna qualification (decisión de diseño ya tomada en Stage 1): aparecen en el resultado de Stage 2 como skills sueltas, pero no afectan la clasificación. 
## Definición formal 
Se modela cada perfil como un DFA independiente, mediante la 5-tupla (Q, Σ, δ, q₀, F): 
- **Q** = conjunto de subconjuntos de las qualifications del perfil (el estado representa "qué qualifications ya están cubiertas"), de la forma que quedan: **Q** = {q0, q1, $\dots$, q_n, qf}
- **Σ** = conjunto de todos los skills normalizados posibles (los del perfil, los del otro perfil, y los opcionales/certificaciones). 
- **δ** = función de transición: δ(S, skill) = S ∪ {qualification(skill)} si *skill* pertenece a una qualification de este perfil; δ(S, skill) = S en caso contrario. 
- **q0** = $\emptyset$ (ninguna qualification cubierta al iniciar), con incio en q0. 
- **F** = {Q_total}, donde Q_total es el conjunto completo de qualifications del perfil (único estado de aceptación: cobertura total). 
## Regla de aceptación
Un candidato queda clasificado en un perfil si y solo si el DFA de ese perfil, al consumir toda la secuencia de skills normalizados del CV, termina en el estado final Q_total (es decir, encontró al menos un skill para cada una de las qualifications del perfil). Full Stack y Cybersecurity se evalúan por separado con esta misma regla. 
## Ejemplo 
Para el fragmento de Laura Gómez (mySQL, React.js $\rightarrow$ normalizados a SQL, REACT): el DFA de Full Stack queda en el estado {Database Management, Frontend Development}, no alcanza Q_total (faltan Backend, API, Version Control), así que no es aceptada por ese perfil con solo esos dos skills.