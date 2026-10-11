import pdfplumber

def pdf_a_texto(ruta_pdf: str) -> str:
    """Abre un PDF y devuelve todo su texto como un solo string,
    con las paginas separadas por una linea en blanco."""
    paginas_texto = []
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                paginas_texto.append(texto_pagina)
    return "\n\n".join(paginas_texto)


def pdf_a_archivo_txt(ruta_pdf: str, ruta_txt: str) -> None:
    """Igual que pdf_a_texto, pero ademas guarda el resultado en un .txt."""
    texto = pdf_a_texto(ruta_pdf)
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write(texto)