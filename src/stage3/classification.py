from itertools import combinations
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol


def _llave(qualifications_cubiertas):
    #Convierte una lista de qualifications cubiertas en una tupla ordenada, para poder usarla como nombre unico de estado.
    return tuple(sorted(set(qualifications_cubiertas)))


def build_dfa_fullstack() -> DeterministicFiniteAutomaton:
    skill_to_qual = {
        "JAVASCRIPT": "FRONTEND DEVELOPMENT", "TYPESCRIPT": "FRONTEND DEVELOPMENT", "REACT": "FRONTEND DEVELOPMENT",
        "ANGULAR": "FRONTEND DEVELOPMENT", "VUE": "FRONTEND DEVELOPMENT",
        "NODE.JS": "BACKEND DEVELOPMENT", "DJANGO": "BACKEND DEVELOPMENT", "SPRING BOOT": "BACKEND DEVELOPMENT",
        "SQL": "DATABASE MANAGEMENT", "NOSQL": "DATABASE MANAGEMENT",
        "APIS REST": "API INTEGRATION",
        "GIT": "VERSION CONTROL",
    }
    qualificaciones = ["FRONTEND DEVELOPMENT", "BACKEND DEVELOPMENT", "DATABASE MANAGEMENT", "API INTEGRATION", "VERSION CONTROL"]
    vocabulario = list(skill_to_qual) + [
        "NMAP", "WIRESHARK", "BURP SUITE", "METASPLOIT",
        "PENETRATION TESTING", "VULNERABILITY ASSESSMENT", "OWASP", "INCIDENT RESPONSE",
        "AWS SECURITY", "AZURE SECURITY", "CEH", "OSCP", "SECURITY+",
    ]
    return _construir_dfa(skill_to_qual, qualificaciones, vocabulario)


def build_dfa_cyber() -> DeterministicFiniteAutomaton:
    skill_to_qual = {
        "NMAP": "SECURITY TOOLS", "WIRESHARK": "SECURITY TOOLS", "BURP SUITE": "SECURITY TOOLS", "METASPLOIT": "SECURITY TOOLS",
        "PENETRATION TESTING": "SECURITY PRACTICES", "VULNERABILITY ASSESSMENT": "SECURITY PRACTICES",
        "OWASP": "SECURITY PRACTICES", "INCIDENT RESPONSE": "SECURITY PRACTICES",
        "AWS SECURITY": "CLOUD SECURITY", "AZURE SECURITY": "CLOUD SECURITY",
        "GIT": "VERSION CONTROL",
    }
    qualificaciones = ["SECURITY TOOLS", "SECURITY PRACTICES", "CLOUD SECURITY", "VERSION CONTROL"]
    vocabulario = list(skill_to_qual) + [
        "JAVASCRIPT", "TYPESCRIPT", "REACT", "ANGULAR", "VUE",
        "NODE.JS", "DJANGO", "SPRING BOOT", "SQL", "NOSQL", "APIS REST",
        "CEH", "OSCP", "SECURITY+",
    ]
    return _construir_dfa(skill_to_qual, qualificaciones, vocabulario)


def _construir_dfa(skill_to_qual, qualificaciones, vocabulario):
    """Genera los 2^n estados (como tuplas ordenadas), les pone nombre secuencial
    q0, q1, ..., qN (el ultimo es el de aceptacion), y arma las transiciones."""
    combinaciones = []
    for k in range(len(qualificaciones) + 1):
        for combo in combinations(qualificaciones, k):
            combinaciones.append(_llave(combo))

    nombre_estado = {combinacion: f"q{i}" for i, combinacion in enumerate(combinaciones)}

    dfa = DeterministicFiniteAutomaton()
    dfa.add_start_state(State(nombre_estado[_llave([])]))
    dfa.add_final_state(State(nombre_estado[_llave(qualificaciones)]))

    for combinacion in combinaciones:
        for skill in vocabulario:
            qual = skill_to_qual.get(skill)
            cubiertas_nuevas = list(combinacion) + ([qual] if qual else [])
            llave_nueva = _llave(cubiertas_nuevas)
            dfa.add_transition(State(nombre_estado[combinacion]), Symbol(skill), State(nombre_estado[llave_nueva]))

    return dfa


def clasifica(dfa: DeterministicFiniteAutomaton, skills_normalizados: list) -> bool:
    return dfa.accepts([Symbol(s) for s in skills_normalizados])


dfa_fullstack = build_dfa_fullstack()
dfa_cyber = build_dfa_cyber()


def clasificar_perfil(skills_normalizados: list) -> dict:
    return {
        "Full Stack Developer": clasifica(dfa_fullstack, skills_normalizados),
        "Cybersecurity Specialist": clasifica(dfa_cyber, skills_normalizados),
    }