"""Text/PDF entry points using the contributor's unchanged PDF reader."""
from pathlib import Path
import tempfile

from src.emmanuel_bridge import load_module


def read_resume(path):
    path = Path(path)
    if path.suffix.lower() == '.txt':
        return path.read_text(encoding='utf-8-sig')
    if path.suffix.lower() != '.pdf':
        raise ValueError('Choose a UTF-8 .txt file or a text-based .pdf file.')
    reader = load_module('resumelens_team_pdf_reader', 'pdfextract.py')
    try:
        text = reader.pdf_a_texto(str(path))
    except OSError:
        raise
    except Exception as error:
        raise ValueError('The PDF could not be read.') from error
    if not text.strip():
        raise ValueError('The PDF has no extractable text. Use a text-based PDF or paste the text.')
    return text


def uploaded_text(data, filename):
    suffix = Path(filename).suffix.lower()
    if suffix == '.txt':
        try:
            return data.decode('utf-8-sig')
        except UnicodeDecodeError as error:
            raise ValueError('Use a UTF-8 text file.') from error
    if suffix != '.pdf':
        raise ValueError('Choose a .txt or .pdf file.')
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / 'resume.pdf'
        path.write_bytes(data)
        return read_resume(path)
