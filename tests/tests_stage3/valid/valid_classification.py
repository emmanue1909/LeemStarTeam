import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from stage3 import classification as clf


def test_fullstack_completo_es_aceptado():
    skills = ["JAVASCRIPT", "NODE.JS", "SQL", "APIS REST", "GIT"]
    resultado = clf.clasificar_perfil(skills)
    assert resultado["Full Stack Developer"] is True


def test_cyber_completo_es_aceptado():
    skills = ["NMAP", "PENETRATION TESTING", "AWS SECURITY", "GIT"]
    resultado = clf.clasificar_perfil(skills)
    assert resultado["Cybersecurity Specialist"] is True


def test_fullstack_acepta_sin_importar_el_orden():
    skills = ["GIT", "APIS REST", "SQL", "NODE.JS", "JAVASCRIPT"]
    resultado = clf.clasificar_perfil(skills)
    assert resultado["Full Stack Developer"] is True


def test_fullstack_acepta_con_skills_repetidos():
    skills = ["JAVASCRIPT", "NODE.JS", "SQL", "APIS REST", "GIT", "GIT", "JAVASCRIPT"]
    resultado = clf.clasificar_perfil(skills)
    assert resultado["Full Stack Developer"] is True


def test_fullstack_ignora_ruido_de_otro_perfil():
    """Mezclar skills de Cybersecurity no debe impedir que Full Stack sea aceptado."""
    skills = ["JAVASCRIPT", "NODE.JS", "SQL", "APIS REST", "GIT", "NMAP", "OWASP"]
    resultado = clf.clasificar_perfil(skills)
    assert resultado["Full Stack Developer"] is True


def test_clasificar_perfil_devuelve_booleanos_para_ambos_perfiles():
    resultado = clf.clasificar_perfil(["JAVASCRIPT"])
    assert set(resultado.keys()) == {"Full Stack Developer", "Cybersecurity Specialist"}
    assert isinstance(resultado["Full Stack Developer"], bool)
    assert isinstance(resultado["Cybersecurity Specialist"], bool)


def test_dfa_fullstack_tiene_2_elevado_a_5_estados():
    """5 qualifications -> 2^5 = 32 estados (uno por cada subconjunto cubierto)."""
    assert len(clf.dfa_fullstack.states) == 32


def test_dfa_cyber_tiene_2_elevado_a_4_estados():
    """4 qualifications -> 2^4 = 16 estados."""
    assert len(clf.dfa_cyber.states) == 16


def test_dfa_fullstack_es_determinista():
    assert clf.dfa_fullstack.is_deterministic()


def test_dfa_cyber_es_determinista():
    assert clf.dfa_cyber.is_deterministic()


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    aprobados = 0
    for test in tests:
        try:
            test()
            print(f"[APROBADO] {test.__name__}")
            aprobados += 1
        except AssertionError as e:
            print(f"[FALLO]    {test.__name__} -> {e}")
    print(f"\n{aprobados}/{len(tests)} tests validos pasados")