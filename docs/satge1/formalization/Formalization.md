Antes de definir los patrones regex, se documentan las decisiones de alcance tomadas por el equipo (siguiendo el mismo enfoque que `decisiones.md` en la Etapa 4):

## Objetivo 
Extraer la información cruda de la hoja de vida (contacto, lenguajes, frameworks, bases de datos, experiencia, certificaciones, etc.) usando el módulo `re` de Python, como entrada para la Etapa 2 (normalización FST).

## Alcances comunes

- **Email:** no se restringe a proveedores específicos (Gmail, Yahoo, Outlook). Se valida únicamente la estructura general `usuario@dominio.tld`, para aceptar también correos corporativos o institucionales (ej. `@icesi.edu.co`). Ejemplo: 'camila.redondo@gmail.com'

- **Teléfono:** formato fijo de 3 grupos separados por guión: `+<código_país>-<código_ciudad>-<número>` (ej. `+57-4-5559876`). No se contemplan otros formatos (celulares sin código de ciudad, espacios en vez de guiones, etc.), porque asi se gestiona el formato en los ejemplos y como se decidio. Ejemplo: '+57-4-5559876'

- **Años de experiencia**: rango (0, 60), sin incluir los extremos — es decir, valores entre 1 y 59. Este rango debe coincidir con el que ya valida `validator.py` en la Etapa 4, para mantener consistencia en todo el pipeline. 

- **Nombre:** string de mínimo 2 y máximo 4 palabras separadas por espacio (ej. "Juan Pérez" con 2, o "Sandra Lorena Muñoz Vela" con 4), cubriendo las combinaciones usuales de nombre(s) + apellido(s) en Colombia. Nombres de 5 o más palabras no se contemplan.
- **Location**:  Para la ubicacion de la persona vamos a filtrar por palabras que rodeen la parte que nos interesa ya que no hay un formato fijo para sacar la ciudad y pais, con estas frases anclas podremos sacarlas, de una forma tal que: "radicada/radicado en `<location>`". Ejemplo: "radicada en Cali, Colombia" -> location = "Cali, Colombia".
- **GitHub**: para el usuario de github tenemos que pueda ser opcional y para este caso tampoco tenemos un formato fijo para el usuario de github por lo que usaremos tambien frases anclas como: "usuario de GitHub es `<github>`". Ejemplo: "usuario de GitHub es lauragomez" -> github = "lauragomez".
- **Position + Company**: Para este caso es un poco mas complejo sin estructura fija y frases anclas menos especificas pero tomaremos el caso simplificado tal que: "mi posicion es `<position>` en la compañia`<company>`". Ejemplo "mi posicion es Security Engineer en la compañia Globant" -> position = "Security Engineer", company = "Globant".
- **Institution + Program**: | "egresada/egresado del programa de `<program>` de la `<institution>`" | "egresada del programa de Ingeniería de Sistemas de la Universidad Icesi" |
## Expresiones por perfil

### Full Stack Developer
| Categoría | Keywords a detectar | Patrón regex | |---|---|---| | Frontend | JavaScript, TypeScript, React, Angular, Vue | _(fase de código)_ | | Backend | Node.js, Django, Spring Boot | _(fase de código)_ | | Bases de datos | SQL, NoSQL | _(fase de código)_ | | Integración | APIs REST | _(fase de código)_ | | Control de versiones | Git | _(fase de código)_ | 
### Cybersecurity Specialist 
| Categoría | Keywords a detectar | Patrón regex | |---|---|---| | Herramientas | Nmap, Wireshark, Burp Suite, Metasploit | _(fase de código)_ | | Prácticas | Penetration Testing, Vulnerability Assessment, OWASP, Incident Response | _(fase de código)_ | | Certificaciones | CEH, OSCP, Security+ | _(fase de código)_ | | Seguridad en la nube | AWS Security, Azure Security | _(fase de código)_ | | Control de versiones | Git | _(fase de código)_ |



