import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from stage2 import normalization as norm


def test_normalizar_variante_desconocida_retorna_none():
    assert norm.normalizar("NO EXISTE", norm.fst_global) is None


def test_normalizar_skill_descarta_coincidencias_no_mapeadas():
    """
    Si un extractor llegara a devolver algo que no esta en la tabla de
    variantes, normalizar_skill debe filtrarlo (no reventar ni dejarlo
    pasar sin normalizar).
    """
    def extractor_dummy(_texto):
        return ["ALGO QUE NO EXISTE"]

    assert norm.normalizar_skill("irrelevante", extractor_dummy) == []


def test_perfil_fullstack_sin_menciones_no_rompe():
    resultado = norm.normalizar_perfil_fullstack("No menciono ninguna tecnologia.")
    assert resultado == {"skills": [], "qualifications": []}


def test_perfil_con_texto_vacio_no_rompe():
    resultado = norm.normalizar_perfil_fullstack("")
    assert resultado == {"skills": [], "qualifications": []}


def test_qualification_nivel_fuera_de_rango_no_llega_normalizado():
    """
    El nivel 9 ya deberia haber sido rechazado por el regex de Stage 1
    (solo acepta 1-5); esto confirma que la cadena completa Stage1->Stage2
    tampoco deja pasar nada para ese caso.
    """
    resultado = norm.normalizar_qualification(
        "Tengo un nivel 9 en Frontend Development.",
        norm.extract_specific.extract_qualifications_frontend_fullstack,
    )
    assert resultado == []


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