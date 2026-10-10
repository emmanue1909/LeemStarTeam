Antes de definir los patrones regex, se documentan las decisiones de alcance tomadas por el equipo (siguiendo el mismo enfoque que `decisiones.md` en la Etapa 4):

## Objetivo 
Extraer la información cruda de la hoja de vida (contacto, lenguajes, frameworks, bases de datos, experiencia, certificaciones, etc.) usando el módulo `re` de Python, como entrada para la Etapa 2 (normalización FST).

## Alcances comunes

- **Email:** no se restringe a proveedores específicos (Gmail, Yahoo, Outlook). Se valida únicamente la estructura general `usuario@dominio.tld`, para aceptar también correos corporativos o institucionales (ej. `@icesi.edu.co`). Ejemplo: 'camila.redondo@gmail.com'

- **Teléfono:** formato fijo de 3 grupos separados por guión: `+<código_país>-<código_ciudad>-<número>` (ej. `+57-4-5559876`). No se contemplan otros formatos (celulares sin código de ciudad, espacios en vez de guiones, etc.), porque asi se gestiona el formato en los ejemplos y como se decidio. Ejemplo: '+57-4-5559876'

- **Años de experiencia**: rango (0, 60), sin incluir los extremos — es decir, valores entre 1 y 59. Este rango debe coincidir con el que ya valida `validator.py` en la Etapa 4, para mantener consistencia en todo el pipeline, con esto en mente vamos a usar la frase ancla: "mi experiencia es de `<years>` años". Ejemplo: "mi experiencia es de 20 años"

- **Nombre:** string de mínimo 2 y máximo 4 palabras separadas por espacio (ej. "Juan Pérez" con 2, o "Sandra Lorena Muñoz Vela" con 4), cubriendo las combinaciones usuales de nombre(s) + apellido(s) en Colombia. Nombres de 5 o más palabras no se contemplan. Usando la frase ancla "mi nombre es `<name>`". Ejemplo: "mi nombre es Juan Pérez"
- **Location**:  Para la ubicacion de la persona vamos a filtrar por palabras que rodeen la parte que nos interesa ya que no hay un formato fijo para sacar la ciudad y pais, con estas frases anclas podremos sacarlas, de una forma tal que: "radicada/radicado en `<location>`". Ejemplo: "radicada en Cali, Colombia" -> location = "Cali, Colombia".
- **GitHub**: para el usuario de github tenemos que pueda ser opcional y para este caso tampoco tenemos un formato fijo para el usuario de github por lo que usaremos tambien frases anclas como: "usuario de GitHub es `<github>`". Ejemplo: "usuario de GitHub es lauragomez" -> github = "lauragomez".
- **Position + Company**: Para este caso es un poco mas complejo sin estructura fija y frases anclas menos especificas pero tomaremos el caso simplificado tal que: "mi posicion es `<position>` en la compañia`<company>`". Ejemplo "mi posicion es Security Engineer en la compañia Globant" -> position = "Security Engineer", company = "Globant".
- **Institution + Program**: Con este caso ocurre lo mismo que hemos venido mencionando anteriormente, entonces usaremos la frase ancla: "egresada/egresado del programa de `<program>` de la `<institution>`". Ejemplo: "egresada del programa de Ingeniería de Sistemas de la Universidad Icesi" 

**NOTA:** las anclas que incluyen participios ("radicada/radicado", "egresada/egresado") deben aceptar ambas terminaciones (`radicad[oa]`, `egresad[oa]`), ya que los candidatos de ejemplo pueden ser hombres o mujeres.
## Expresiones por perfil

**Skills y qualifications (todos los perfiles):** la detección es insensible a mayúsculas/minúsculas — "react", "React" y "REACT" cuentan como la misma coincidencia, siempre que corresponda a una skill de la lista conocida.

**Nota de diseño:** para que un ejemplo cuente como "válido" para un perfil, no basta con mencionar varias skills — el candidato debe cubrir todas las categorías de ese perfil (ver la regla de aceptación mínima definida en `docs/stage3_automata/formalizacion.md`). Esto afecta cómo se redactan los párrafos de ejemplo de esta etapa.

## PERFILES
### Full Stack Developer
#### Skills (específicos, sin nivel) 
- JavaScript 
- TypeScript
- React
- Angular
- Vue
- Node.js
- Django
- Spring Boot
- SQL 
- NoSQL
- APIs REST
- Git 
#### Qualifications (áreas de dominio, con nivel 1-5)
- Frontend Development
- Backend Development
- Database Management
- API Integration
- Version Control

**NOTA:** Para las qualifications para obtener su nivel ya que es un int usaremos una frase ancla: "tengo un nivel `<level>` en `<qualification>`". Ejemplo: "tengo un nivel 4 en Frontend Development".
### Cybersecurity Specialist 
#### Skills (específicos, sin nivel)
- Nmap 
- Wireshark
- Burp Suite
- Metasploit
- Penetration Testing
- Vulnerability Assessment
- OWASP
- Incident Response
- AWS Security
- Azure Security
- Git
- CEH
- OSCP
- Security+ 
#### Qualifications (áreas de dominio, con nivel 1-5)
- Security Tools
- Security Practices
- Cloud Security
- Version Control
**NOTA:** CEH, OSCP y Security+ son certificaciones, no se agrupan bajo ninguna qualification — se extraen como skills normales pero son opcionales: no cuentan para ninguna categoría de la regla de aceptación mínima (ver `docs/stage3_automata/formalizacion.md`), a diferencia de las demás skills que sí pertenecen a una de las 4 qualifications (Security Tools, Security Practices, Cloud Security, Version Control). De igual forma para las qualifications para obtener su nivel ya que es un int usaremos una frase ancla: "tengo un nivel `<level>` en `<qualification>`"

## Abreviaciones y variantes reconocidas

Además de la detección insensible a mayúsculas/minúsculas, para cada skill se contemplan las variantes reales con las que suele aparecer escrita en una hoja de vida. Stage 1 captura el texto crudo tal como aparece (la variante), y es la Etapa 2 (FST) la que la normaliza a la forma canónica — ver `docs/stage2_fst/formalizacion.md`.

### Full Stack Developer

| Skill (canónico) | Variantes reconocidas                      |
| ---------------- | ------------------------------------------ |
| JavaScript       | JavaScript, Java Script, JS                |
| TypeScript       | TypeScript, Type Script, TS                |
| React            | React, React.js, ReactJS                   |
| Angular          | Angular, AngularJS                         |
| Vue              | Vue, Vue.js, VueJS                         |
| Node.js          | Node.js, Node, NodeJS                      |
| Django           | Django                                     |
| Spring Boot      | Spring Boot, SpringBoot                    |
| SQL              | SQL, MySQL, PostgreSQL, Postgres           |
| NoSQL            | NoSQL, MongoDB, Mongo                      |
| APIs REST        | APIs REST, API REST, REST API, RESTful API |
| Git              | Git                                        |

### Cybersecurity Specialist

| Skill (canónico) | Variantes reconocidas |
|---|---|
| Nmap | Nmap, Network Mapper |
| Wireshark | Wireshark |
| Burp Suite | Burp Suite, BurpSuite, Burp |
| Metasploit | Metasploit, Metasploit Framework |
| Penetration Testing | Penetration Testing, Pentesting, PenTest, Pentest |
| Vulnerability Assessment | Vulnerability Assessment |
| OWASP | OWASP, Open Web Application Security Project |
| Incident Response | Incident Response |
| AWS Security | AWS Security, Amazon Web Services Security |
| Azure Security | Azure Security, Microsoft Azure Security |
| Git | Git |
| CEH | CEH, Certified Ethical Hacker |
| OSCP | OSCP, Offensive Security Certified Professional |
| Security+ | Security+, CompTIA Security+ |

## Decisiones de diseño — alcance de variantes

- **Spring Boot**: no se contempla "Spring" solo como variante — también es una palabra común (la estación, un manantial), y aceptarla sola arriesgaría falsos positivos.
- **Git**: no se contempla GitHub ni GitLab como variantes — son plataformas de alojamiento, no la herramienta de control de versiones en sí; son conceptos relacionados pero distintos.
- **AWS Security / Azure Security**: no se contempla "AWS" ni "Azure" solos — alguien puede tener experiencia en esas nubes sin que sea específicamente de seguridad, y aceptarlos solos clasificaría mal esa experiencia como la skill de seguridad.