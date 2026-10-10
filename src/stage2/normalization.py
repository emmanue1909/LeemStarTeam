from pyformlang.fst import FST
from stage1 import extract_specific

#Diccionario para cada clave:[datos] -> skill_canonica:[posibles_entradas] e igual para cada qualification

#Skills full stack
variantes_skills_fullstack = {
    "JAVASCRIPT":  ["JAVASCRIPT", "JAVA SCRIPT", "JS"],
    "TYPESCRIPT":  ["TYPESCRIPT", "TYPE SCRIPT", "TS"],
    "REACT":       ["REACT.JS", "REACTJS", "REACT"],
    "ANGULAR":     ["ANGULARJS", "ANGULAR"],
    "VUE":         ["VUE.JS", "VUEJS", "VUE"],
    "NODE.JS":     ["NODE.JS", "NODEJS", "NODE"],
    "DJANGO":      ["DJANGO"],
    "SPRING BOOT": ["SPRING BOOT", "SPRINGBOOT"],
    "SQL":         ["POSTGRESQL", "MYSQL", "POSTGRES", "SQL"],
    "NOSQL":       ["NOSQL", "MONGODB", "MONGO"],
    "APIS REST":   ["RESTFUL API", "APIS REST", "API REST", "REST API"],
    "GIT":         ["GIT"],
}

#Qualifications full stack
variantes_qualifications_fullstack = {
    "FRONTEND DEVELOPMENT": ["FRONTEND DEVELOPMENT"],
    "BACKEND DEVELOPMENT":  ["BACKEND DEVELOPMENT"],
    "DATABASE MANAGEMENT":  ["DATABASE MANAGEMENT"],
    "API INTEGRATION":      ["API INTEGRATION"],
    "VERSION CONTROL":      ["VERSION CONTROL"],
}

#Skills cybersecurity
variantes_skills_cyber = {
    "NMAP":                     ["NETWORK MAPPER", "NMAP"],
    "WIRESHARK":                ["WIRESHARK"],
    "BURP SUITE":               ["BURP SUITE", "BURPSUITE", "BURP"],
    "METASPLOIT":               ["METASPLOIT FRAMEWORK", "METASPLOIT"],
    "PENETRATION TESTING":      ["PENETRATION TESTING", "PENTESTING", "PENTEST"],
    "VULNERABILITY ASSESSMENT": ["VULNERABILITY ASSESSMENT"],
    "OWASP":                    ["OPEN WEB APPLICATION SECURITY PROJECT", "OWASP"],
    "INCIDENT RESPONSE":        ["INCIDENT RESPONSE"],
    "AWS SECURITY":             ["AMAZON WEB SERVICES SECURITY", "AWS SECURITY"],
    "AZURE SECURITY":           ["MICROSOFT AZURE SECURITY", "AZURE SECURITY"],
    "GIT":                      ["GIT"],
    "CEH":                      ["CERTIFIED ETHICAL HACKER", "CEH"],
    "OSCP":                     ["OFFENSIVE SECURITY CERTIFIED PROFESSIONAL", "OSCP"],
    "SECURITY+":                ["COMPTIA SECURITY+", "SECURITY+"],
}

#Qualifications cybersecurity
variantes_qualifications_cyber = {
    "SECURITY TOOLS":     ["SECURITY TOOLS"],
    "SECURITY PRACTICES": ["SECURITY PRACTICES"],
    "CLOUD SECURITY":     ["CLOUD SECURITY"],
    "VERSION CONTROL":    ["VERSION CONTROL"],
}

#Tabla total
tabla_variantes = {
    **variantes_skills_fullstack,
    **variantes_qualifications_fullstack,
    **variantes_skills_cyber,
    **variantes_qualifications_cyber,
}

def build_normalizer(tabla: dict) -> FST:
    fst = FST()
    fst.add_start_state('q0')
    fst.add_final_state('qf')
    for canonico, variantes in tabla.items():
        for variante in variantes:
            fst.add_transition('q0', variante.upper(), 'qf', [canonico])
    return fst


def normalizar(variante_cruda: str, fst: FST):
    resultado = list(fst.translate([variante_cruda.upper()]))
    return resultado[0][0] if resultado else None


fst_global = build_normalizer(tabla_variantes)

def normalizar_skill(text, extractor):
    """extractor: una funcion extract_skill_* (devuelve lista de strings)."""
    matches = extractor(text)
    normalizados = [normalizar(m, fst_global) for m in matches]
    return [n for n in normalizados if n is not None]


def normalizar_qualification(text, extractor):
    """extractor: una funcion extract_qualifications_* (devuelve lista de tuplas (nivel, nombre))."""
    matches = extractor(text)
    resultado = []
    for nivel, nombre in matches:
        canonico = normalizar(nombre, fst_global)
        if canonico:
            resultado.append((nivel, canonico))
    return resultado


# ---------- listas de extractores por perfil ----------

SKILLS_FULLSTACK = [
    extract_specific.extract_skill_javascript,
    extract_specific.extract_skill_typescript,
    extract_specific.extract_skill_react,
    extract_specific.extract_skill_angular,
    extract_specific.extract_skill_vue,
    extract_specific.extract_skill_nodejs,
    extract_specific.extract_skill_django,
    extract_specific.extract_skill_springboot,
    extract_specific.extract_skill_sql,
    extract_specific.extract_skill_nosql,
    extract_specific.extract_skill_apis_rest,
    extract_specific.extract_skill_git,
]

QUALIFICATIONS_FULLSTACK = [
    extract_specific.extract_qualifications_frontend_fullstack,
    extract_specific.extract_qualifications_backend_fullstack,
    extract_specific.extract_qualifications_database_fullstack,
    extract_specific.extract_qualifications_api_fullstack,
    extract_specific.extract_qualifications_versioncontrol_fullstack,
]

SKILLS_CYBER = [
    extract_specific.extract_skill_nmap,
    extract_specific.extract_skill_wireshark,
    extract_specific.extract_skill_burpsuite,
    extract_specific.extract_skill_metasploit,
    extract_specific.extract_skill_pentest,
    extract_specific.extract_skill_vulnassessment,
    extract_specific.extract_skill_owasp,
    extract_specific.extract_skill_incidentresponse,
    extract_specific.extract_skill_awssecurity,
    extract_specific.extract_skill_azuresecurity,
    extract_specific.extract_skill_git_cyber,
    extract_specific.extract_skill_ceh,
    extract_specific.extract_skill_oscp,
    extract_specific.extract_skill_securityplus,
]

QUALIFICATIONS_CYBER = [
    extract_specific.extract_qualifications_securitytools_cyber,
    extract_specific.extract_qualifications_securitypractices_cyber,
    extract_specific.extract_qualifications_cloudsecurity_cyber,
    extract_specific.extract_qualifications_versioncontrol_cyber,
]


# ---------- funcion final por perfil ----------

def normalizar_perfil_fullstack(text):
    skills = []
    for extractor in SKILLS_FULLSTACK:
        skills.extend(normalizar_skill(text, extractor))

    qualifications = []
    for extractor in QUALIFICATIONS_FULLSTACK:
        qualifications.extend(normalizar_qualification(text, extractor))

    return {"skills": skills, "qualifications": qualifications}


def normalizar_perfil_cyber(text):
    skills = []
    for extractor in SKILLS_CYBER:
        skills.extend(normalizar_skill(text, extractor))

    qualifications = []
    for extractor in QUALIFICATIONS_CYBER:
        qualifications.extend(normalizar_qualification(text, extractor))

    return {"skills": skills, "qualifications": qualifications}