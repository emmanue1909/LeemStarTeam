def _esc(valor: str) -> str:
    return str(valor).replace('"', '\\"')

def construir_resume_dsl(datos: dict) -> str:
    lineas = []
    lineas.append(f'name "{_esc(datos["nombre"])}" location "{_esc(datos["ubicacion"])}"')

    linea_contacto = f'email "{_esc(datos["email"])}"'
    if datos.get("github"):
        linea_contacto += f' github "{_esc(datos["github"])}"'
    lineas.append(linea_contacto)

    for exp in datos.get("experiencias", []):
        lineas.append(f'position "{_esc(exp["position"])}" company "{_esc(exp["company"])}" years {int(exp["years"])}')

    for edu in datos.get("educaciones", []):
        lineas.append(f'institution "{_esc(edu["institucion"])}" phone "{_esc(edu["phone"])}" program "{_esc(edu["program"])}"')

    skills_unicas = list(dict.fromkeys(datos.get("skills", [])))
    for skill in skills_unicas:
        lineas.append(f'skill "{_esc(skill)}"')

    quals_unicas = list(dict.fromkeys(datos.get("qualifications", [])))
    for nivel, nombre in quals_unicas:
        lineas.append(f'qualification "{_esc(nombre)}" level {int(nivel)}')

    # sin comillas: AcceptedProfile es un literal, no un STRING
    for etiqueta in datos.get("clasificaciones_aceptadas", []):
        lineas.append(f'classification {etiqueta}')

    return "\n".join(lineas) + "\n"