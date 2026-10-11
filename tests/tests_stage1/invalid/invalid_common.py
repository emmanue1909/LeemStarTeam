import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage1.extract_common import (
    extract_email, extract_phone, extract_experience_years, extract_name,
    extract_location, extract_github, extract_position_company, extract_institution_program,
)


def test_email_ausente():
    assert extract_email("No deje ningun contacto aqui.") is None


def test_telefono_con_un_digito_de_mas_no_matchea():
    assert extract_phone("Mi telefono es +57-3-12345678") is None


def test_telefono_con_un_digito_de_menos_no_matchea():
    assert extract_phone("Mi telefono es +57-3-123456") is None


def test_telefono_ausente():
    assert extract_phone("No tengo numero registrado.") is None


def test_anios_experiencia_fuera_de_rango_60_no_matchea():
    assert extract_experience_years("Mi experiencia es de 60 años.") is None


def test_anios_experiencia_ausente():
    assert extract_experience_years("No menciono mi experiencia.") is None


def test_nombre_ausente():
    assert extract_name("No quise dar mi nombre.") is None


def test_ubicacion_ausente():
    assert extract_location("No dije donde vivo.") is None


def test_github_ausente():
    assert extract_github("No tengo GitHub.") is None


def test_posicion_y_compania_ausentes():
    assert extract_position_company("No menciono donde trabajo.") == (None, None)


def test_institucion_y_programa_ausentes():
    assert extract_institution_program("No estudie en ningun lado.") == (None, None)


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