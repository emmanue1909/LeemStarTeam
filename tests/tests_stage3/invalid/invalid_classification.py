import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from stage3 import classification as clf


def test_lista_vacia_no_clasifica_a_nadie():
    resultado = clf.clasificar_perfil([])
    assert resultado["Full Stack Developer"] is False
    assert resultado["Cybersecurity Specialist"] is False


def test_fullstack_sin_version_control_no_es_aceptado():
    """Cubre las otras 4 qualifications pero le falta Version Control (Git)."""
    skills = ["JAVASCRIPT", "NODE.JS", "SQL", "APIS REST"]
    resultado = clf.clasificar_perfil(skills)
    assert resultado["Full Stack Developer"] is False


def test_solo_una_qualification_no_alcanza():
    """3 variantes de frontend solo cubren 1 de las 5 qualifications."""
    skills = ["JAVASCRIPT", "TYPESCRIPT", "REACT"]
    resultado = clf.clasificar_perfil(skills)
    assert resultado["Full Stack Developer"] is False


def test_solo_git_no_clasifica_para_ningun_perfil():
    resultado = clf.clasificar_perfil(["GIT"])
    assert resultado["Full Stack Developer"] is False
    assert resultado["Cybersecurity Specialist"] is False


def test_candidato_cyber_no_es_fullstack_aunque_use_git():
    """Version Control (Git) es compartido, pero sin el resto de skills
    de Full Stack, ese candidato de Cybersecurity no debe calificar."""
    skills = ["NMAP", "PENETRATION TESTING", "AWS SECURITY", "GIT"]
    resultado = clf.clasificar_perfil(skills)
    assert resultado["Full Stack Developer"] is False


def test_simbolo_desconocido_no_rompe_la_clasificacion():
    resultado = clf.clasificar_perfil(["SKILL_QUE_NO_EXISTE"])
    assert resultado["Full Stack Developer"] is False
    assert resultado["Cybersecurity Specialist"] is False


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
    print(f"\n{aprobados}/{len(tests)} tests invalidos pasados")