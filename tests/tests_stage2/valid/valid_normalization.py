import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from stage2 import normalization as norm


# ---------- Normalizacion de variantes individuales ----------

def test_normaliza_variante_con_punto():
    assert norm.normalizar("react.js", norm.fst_global) == "REACT"


def test_normaliza_sigla_js():
    assert norm.normalizar("JS", norm.fst_global) == "JAVASCRIPT"


def test_normaliza_variante_nodejs_junto():
    assert norm.normalizar("NODEJS", norm.fst_global) == "NODE.JS"


def test_normaliza_variante_node_sola():
    assert norm.normalizar("NODE", norm.fst_global) == "NODE.JS"


def test_normalizar_es_insensible_a_mayusculas():
    assert norm.normalizar("database management", norm.fst_global) == "DATABASE MANAGEMENT"


def test_normaliza_variante_con_caracter_especial():
    assert norm.normalizar("Security+", norm.fst_global) == "SECURITY+"


# ---------- Integracion extractor + FST ----------

def test_normalizar_skill_integra_extractor_y_fst():
    texto = "Trabajo con React.js y Node.js."
    resultado = norm.normalizar_skill(texto, norm.extract_specific.extract_skill_react)
    assert resultado == ["REACT"]


def test_normalizar_qualification_integra_extractor_y_fst():
    texto = "Tengo un nivel 4 en Frontend Development."
    resultado = norm.normalizar_qualification(
        texto, norm.extract_specific.extract_qualifications_frontend_fullstack
    )
    assert resultado == [("4", "FRONTEND DEVELOPMENT")]


def test_perfil_fullstack_combina_skills_y_qualifications():
    texto = "Uso JavaScript, React.js y Git. Tengo un nivel 4 en Frontend Development."
    resultado = norm.normalizar_perfil_fullstack(texto)
    assert resultado == {
        "skills": ["JAVASCRIPT", "REACT", "GIT"],
        "qualifications": [("4", "FRONTEND DEVELOPMENT")],
    }


def test_perfil_cyber_detecta_varias_skills_y_qualification():
    texto = "Uso Git y Nmap. Tengo un nivel 3 en Security Tools."
    resultado = norm.normalizar_perfil_cyber(texto)
    assert resultado == {
        "skills": ["NMAP", "GIT"],
        "qualifications": [("3", "SECURITY TOOLS")],
    }


def test_git_no_se_deduplica_entre_perfiles():
    """
    Stage 2 normaliza cada perfil por separado: si el CV menciona Git,
    tanto el perfil Full Stack como el Cybersecurity lo van a incluir.
    La deduplicacion entre perfiles es responsabilidad de una etapa
    posterior (Stage 4), no de esta.
    """
    texto = "Uso Git para versionar todo."
    fullstack = norm.normalizar_perfil_fullstack(texto)
    cyber = norm.normalizar_perfil_cyber(texto)
    assert "GIT" in fullstack["skills"]
    assert "GIT" in cyber["skills"]


# ---------- El FST en si mismo ----------

def test_fst_global_tiene_un_unico_estado_inicial_y_final():
    assert norm.fst_global.start_states == {"q0"}
    assert norm.fst_global.final_states == {"qf"}


def test_build_normalizer_crea_una_transicion_por_variante():
    tabla_pequena = {"X": ["A", "B"], "Y": ["C"]}
    fst = norm.build_normalizer(tabla_pequena)
    assert fst.get_number_transitions() == 3


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