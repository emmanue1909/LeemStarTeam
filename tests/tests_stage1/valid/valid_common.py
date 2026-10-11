import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.stage1.extract_common import (
    extract_email, extract_phone, extract_experience_years, extract_name,
    extract_location, extract_github, extract_position_company, extract_institution_program,
)


def test_email_valido():
    assert extract_email("Mi correo es laura.gomez@email.com") == "laura.gomez@email.com"


def test_email_con_guion_en_dominio():
    assert extract_email("contacto: laura_2024@mi-empresa.co") == "laura_2024@mi-empresa.co"


def test_telefono_valido():
    assert extract_phone("Mi telefono es +57-3-1234567") == "+57-3-1234567"


def test_anios_experiencia_valido():
    assert extract_experience_years("Mi experiencia es de 3 años.") == "3"


def test_anios_experiencia_limite_superior_25():
    assert extract_experience_years("Mi experiencia es de 25 años.") == "25"


def test_anios_experiencia_con_mayuscula_inicial():
    assert extract_experience_years("Mi experiencia es de 5 años.") == "5"


def test_nombre_valido_dos_palabras():
    assert extract_name("Mi nombre es Laura Gomez.") == "Laura Gomez"


def test_nombre_con_mayuscula_inicial_de_oracion():
    assert extract_name("Mi nombre es Ana Torres.") == "Ana Torres"


def test_nombre_con_cuatro_palabras():
    assert extract_name("mi nombre es Laura Gomez Andrea Ruiz.") == "Laura Gomez Andrea Ruiz"


def test_ubicacion_valida():
    assert extract_location("Estoy radicada en Cali, Colombia.") == "Cali, Colombia"


def test_ubicacion_masculino():
    assert extract_location("Estoy radicado en Bogota.") == "Bogota"


def test_ubicacion_toma_todo_hasta_el_punto():
    assert extract_location("Estoy radicada en Cali, Colombia y trabajo remoto.") == "Cali, Colombia y trabajo remoto"


def test_github_valido():
    assert extract_github("Mi usuario de GitHub es lauragomez123") == "lauragomez123"


def test_github_con_guiones():
    assert extract_github("Mi usuario de GitHub es laura-gomez-dev") == "laura-gomez-dev"


def test_posicion_y_compania_validas():
    assert extract_position_company(
        "Mi posición es Full Stack Developer en la compañía TechCorp."
    ) == ("Full Stack Developer", "TechCorp")


def test_institucion_y_programa_validos():
    assert extract_institution_program(
        "Soy egresada del programa de Ingeniería de Sistemas de la Universidad Icesi."
    ) == ("Ingeniería de Sistemas", "Universidad Icesi")


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