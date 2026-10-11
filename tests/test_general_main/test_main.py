import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from main import procesar_cv

# tests/test_general_main/test_main_pipeline.py -> parents[1] = tests/
_PDFS_DIR = Path(__file__).resolve().parents[1]


def test_candidato_fullstack_valido_genera_reporte():
    pdf = _PDFS_DIR / "1_full_stack_developer.pdf"
    resultado = procesar_cv(str(pdf))

    assert resultado["clasificacion"]["Full Stack Developer"] is True
    assert "Full Stack Developer" in resultado["aceptados"]
    assert resultado["errores_validacion"] == []
    assert resultado["markdown"] is not None
    assert "Laura Gomez" in resultado["markdown"]
    assert "Full Stack Developer" in resultado["markdown"]


def test_candidato_cyber_valido_genera_reporte():
    pdf = _PDFS_DIR / "2_cybersecurity_specialist.pdf"
    resultado = procesar_cv(str(pdf))

    assert resultado["clasificacion"]["Cybersecurity Specialist"] is True
    assert "Cybersecurity Specialist" in resultado["aceptados"]
    assert resultado["errores_validacion"] == []
    assert resultado["markdown"] is not None
    assert "Mariana Ruiz" in resultado["markdown"]


def test_candidato_califica_para_ambos_perfiles():
    pdf = _PDFS_DIR / "3_ambos_perfiles.pdf"
    resultado = procesar_cv(str(pdf))

    assert resultado["clasificacion"]["Full Stack Developer"] is True
    assert resultado["clasificacion"]["Cybersecurity Specialist"] is True
    assert set(resultado["aceptados"]) == {"Full Stack Developer", "Cybersecurity Specialist"}
    assert resultado["errores_validacion"] == []
    assert resultado["markdown"] is not None
    assert "Full Stack Developer" in resultado["markdown"]
    assert "Cybersecurity Specialist" in resultado["markdown"]


def test_candidato_no_califica_no_intenta_stage4():
    pdf = _PDFS_DIR / "4_no_califica.pdf"
    resultado = procesar_cv(str(pdf))

    assert all(valor is False for valor in resultado["clasificacion"].values())
    assert resultado["aceptados"] == []
    assert resultado["markdown"] is None
    assert resultado["errores_validacion"] is None  # ni siquiera se intento Stage 4


def test_candidato_califica_pero_sin_datos_obligatorios():
    pdf = _PDFS_DIR / "5_sin_datos_obligatorios.pdf"
    resultado = procesar_cv(str(pdf))

    assert "Full Stack Developer" in resultado["aceptados"]
    assert resultado["markdown"] is None
    assert resultado["errores_validacion"]  # debe quedar un mensaje de error
    assert "datos obligatorios" in resultado["errores_validacion"][0]


def test_candidato_califica_pero_sin_anios_no_rompe_el_pipeline():
    """
    """
    pdf = _PDFS_DIR / "6_sin_anios.pdf"
    resultado = procesar_cv(str(pdf))

    assert "Full Stack Developer" in resultado["aceptados"]
    assert resultado["markdown"] is None
    assert resultado["errores_validacion"]


def test_dos_candidatos_seguidos_no_se_mezclan():
    """Corre dos CVs distintos en la misma ejecucion y confirma que los
    resultados no comparten estado entre si (los DFA/FST son globales)."""
    resultado_fs = procesar_cv(str(_PDFS_DIR / "1_full_stack_developer.pdf"))
    resultado_sin_perfil = procesar_cv(str(_PDFS_DIR / "4_no_califica.pdf"))

    assert resultado_fs["aceptados"] == ["Full Stack Developer"]
    assert resultado_sin_perfil["aceptados"] == []


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
        except Exception as e:
            print(f"[FALLO]    {test.__name__} -> {type(e).__name__}: {e}")
    print(f"\n{aprobados}/{len(tests)} tests del main pasados")