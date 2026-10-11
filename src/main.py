import sys
from pathlib import Path

from pdfextract import pdf_a_texto
from stage1.extract_specific import (
    extract_email, extract_phone, extract_experience_years, extract_name,
    extract_location, extract_github, extract_position_company, extract_institution_program,
)
from stage2.normalization import normalizar_perfil_fullstack, normalizar_perfil_cyber
from stage3.classification import clasificar_perfil
from stage4.assembler import construir_resume_dsl
from stage4.validator import mm, validate
from stage4.markdown_generator import render_markdown
from textx.exceptions import TextXSyntaxError


def procesar_cv(ruta_pdf: str) -> dict:
    texto = pdf_a_texto(ruta_pdf)

    # --- datos personales (Stage 1) ---
    nombre = extract_name(texto)
    ubicacion = extract_location(texto)
    email = extract_email(texto)
    telefono = extract_phone(texto)
    github = extract_github(texto)
    anios = extract_experience_years(texto)
    posicion, compania = extract_position_company(texto)
    programa, institucion = extract_institution_program(texto)

    # --- skills/qualifications normalizados (Stage 1 + 2) ---
    perfil_fs = normalizar_perfil_fullstack(texto)
    perfil_cy = normalizar_perfil_cyber(texto)
    todos_skills = perfil_fs["skills"] + perfil_cy["skills"]
    todas_quals = perfil_fs["qualifications"] + perfil_cy["qualifications"]

    # --- clasificacion (Stage 3) ---
    clasificacion = clasificar_perfil(todos_skills)
    aceptados = [perfil for perfil, ok in clasificacion.items() if ok]

    resultado = {
        "archivo": ruta_pdf,
        "nombre": nombre,
        "clasificacion": clasificacion,
        "aceptados": aceptados,
        "markdown": None,
        "errores_validacion": None,
    }

    # --- Stage 4: SOLO si califico para al menos un perfil ---
    if not aceptados:
        return resultado

    datos = {
        "nombre": nombre,
        "ubicacion": ubicacion,
        "email": email,
        "github": github,
        "experiencias": [{"position": posicion, "company": compania, "years": anios}] if posicion else [],
        "educaciones": [{"institucion": institucion, "phone": telefono, "program": programa}] if institucion else [],
        "skills": todos_skills,
        "qualifications": todas_quals,
        "clasificaciones_aceptadas": aceptados,
    }
    texto_dsl = construir_resume_dsl(datos)
    try:
        modelo = mm.model_from_str(texto_dsl)
    except TextXSyntaxError as e:
        # pasa cuando faltan datos obligatorios (ej. no se detecto
        # "posicion/compania" o "institucion/programa" en el texto)
        resultado["errores_validacion"] = [f"No se pudo construir el perfil (faltan datos obligatorios): {e}"]
        return resultado

    errores = validate(modelo)
    resultado["errores_validacion"] = errores
    if not errores:
        resultado["markdown"] = render_markdown(modelo)

    return resultado


def imprimir_resultado(resultado: dict) -> None:
    print(f"\n=== {resultado['archivo']} ({resultado['nombre']}) ===")
    print("Clasificacion:", resultado["clasificacion"])

    if not resultado["aceptados"]:
        print("-> No califica para ningun perfil. No se genero reporte.")
        return

    if resultado["errores_validacion"]:
        print("-> Datos invalidos, no se genero el reporte:")
        for err in resultado["errores_validacion"]:
            print(f"   - {err}")
        return

    out = Path("output") / (Path(resultado["archivo"]).stem + ".md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(resultado["markdown"], encoding="utf-8")
    print(f"-> Reporte generado: {out}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.pdf | carpeta_con_pdfs>")
        sys.exit(1)

    ruta = Path(sys.argv[1])

    if ruta.is_dir():
        pdfs = sorted(ruta.glob("*.pdf"))
        if not pdfs:
            print(f"No hay archivos .pdf en {ruta}")
            sys.exit(1)
        for pdf in pdfs:
            imprimir_resultado(procesar_cv(str(pdf)))
    else:
        imprimir_resultado(procesar_cv(str(ruta)))


if __name__ == "__main__":
    main()