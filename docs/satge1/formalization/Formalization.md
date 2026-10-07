Antes de definir los patrones regex, se documentan las decisiones de alcance tomadas por el equipo (siguiendo el mismo enfoque que `decisiones.md` en la Etapa 4):

## Objetivo 
Extraer la información cruda de la hoja de vida (contacto, lenguajes, frameworks, bases de datos, experiencia, certificaciones, etc.) usando el módulo `re` de Python, como entrada para la Etapa 2 (normalización FST).

## Alcances comunes

- **Email:** no se restringe a proveedores específicos (Gmail, Yahoo, Outlook). Se valida únicamente la estructura general `usuario@dominio.tld`, para aceptar también correos corporativos o institucionales (ej. `@icesi.edu.co`). Ejemplo: 'camila.redondo@gmail.com'

- **Teléfono:** formato fijo de 3 grupos separados por guión: `+<código_país>-<código_ciudad>-<número>` (ej. `+57-4-5559876`). No se contemplan otros formatos (celulares sin código de ciudad, espacios en vez de guiones, etc.), porque asi se gestiona el formato en los ejemplos y como se decidio. Ejemplo: '+57-4-5559876'

- **Años de experiencia**: rango (0, 60), sin incluir los extremos — es decir, valores entre 1 y 59. Este rango debe coincidir con el que ya valida `validator.py` en la Etapa 4, para mantener consistencia en todo el pipeline. 

- **Nombre:** string de mínimo 2 y máximo 4 palabras separadas por espacio (ej. "Juan Pérez" con 2, o "Sandra Lorena Muñoz Vela" con 4), cubriendo las combinaciones usuales de nombre(s) + apellido(s) en Colombia. Nombres de 5 o más palabras no se contemplan.



