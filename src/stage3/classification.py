# stage3_automata/classify.py

from itertools import combinations
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol


def subconjuntos(s):
    """Genera todos los subconjuntos de un conjunto (los estados del DFA)."""
    s = list(s)
    for r in range(len(s) + 1):
        for combo in combinations(s, r):
            yield frozenset(combo)


def build_dfa_fullstack() -> DeterministicFiniteAutomaton:
    skill_to_qual = {
        "JAVASCRIPT": "FRONTEND DEVELOPMENT", "TYPESCRIPT": "FRONTEND DEVELOPMENT", "REACT": "FRONTEND DEVELOPMENT",
        "ANGULAR": "FRONTEND DEVELOPMENT", "VUE": "FRONTEND DEVELOPMENT",
        "NODE.JS": "BACKEND DEVELOPMENT", "DJANGO": "BACKEND DEVELOPMENT", "SPRING BOOT": "BACKEND DEVELOPMENT",
        "SQL": "DATABASE MANAGEMENT", "NOSQL": "DATABASE MANAGEMENT",
        "APIS REST": "API INTEGRATION",
        "GIT": "VERSION CONTROL",
    }
    qualificaciones = set(skill_to_qual.values())
    # vocabulario: los skills propios + los del otro perfil y opcionales (para que hagan "bucle")
    vocabulario = list(skill_to_qual) + [
        "NMAP", "WIRESHARK", "BURP SUITE", "METASPLOIT",
        "PENETRATION TESTING", "VULNERABILITY ASSESSMENT", "OWASP", "INCIDENT RESPONSE",
        "AWS SECURITY", "AZURE SECURITY", "CEH", "OSCP", "SECURITY+",
    ]

    dfa = DeterministicFiniteAutomaton()
    dfa.add_start_state(State(frozenset()))
    dfa.add_final_state(State(frozenset(qualificaciones)))

    for estado in subconjuntos(qualificaciones):
        for skill in vocabulario:
            qual = skill_to_qual.get(skill)
            nuevo_estado = estado | {qual} if qual else estado
            dfa.add_transition(State(estado), Symbol(skill), State(frozenset(nuevo_estado)))

    return dfa


def build_dfa_cyber() -> DeterministicFiniteAutomaton:
    skill_to_qual = {
        "NMAP": "SECURITY TOOLS", "WIRESHARK": "SECURITY TOOLS", "BURP SUITE": "SECURITY TOOLS", "METASPLOIT": "SECURITY TOOLS",
        "PENETRATION TESTING": "SECURITY PRACTICES", "VULNERABILITY ASSESSMENT": "SECURITY PRACTICES",
        "OWASP": "SECURITY PRACTICES", "INCIDENT RESPONSE": "SECURITY PRACTICES",
        "AWS SECURITY": "CLOUD SECURITY", "AZURE SECURITY": "CLOUD SECURITY",
        "GIT": "VERSION CONTROL",
    }
    qualificaciones = set(skill_to_qual.values())
    vocabulario = list(skill_to_qual) + [
        "JAVASCRIPT", "TYPESCRIPT", "REACT", "ANGULAR", "VUE",
        "NODE.JS", "DJANGO", "SPRING BOOT", "SQL", "NOSQL", "APIS REST",
        "CEH", "OSCP", "SECURITY+",
    ]

    dfa = DeterministicFiniteAutomaton()
    dfa.add_start_state(State(frozenset()))
    dfa.add_final_state(State(frozenset(qualificaciones)))

    for estado in subconjuntos(qualificaciones):
        for skill in vocabulario:
            qual = skill_to_qual.get(skill)
            nuevo_estado = estado | {qual} if qual else estado
            dfa.add_transition(State(estado), Symbol(skill), State(frozenset(nuevo_estado)))

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