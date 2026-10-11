from io import BytesIO
from pathlib import Path
import tempfile
import unittest

from reportlab.pdfgen.canvas import Canvas

from src.data_app import analyze_text, process_file
from src.resume_input import uploaded_text

ROOT = Path(__file__).resolve().parents[2]


def pdf_bytes(text):
    output = BytesIO()
    canvas = Canvas(output, pagesize=(1500, 1000))
    canvas.setFont('Helvetica', 12)
    for index, line in enumerate(text.splitlines()):
        canvas.drawString(35, 950 - index * 20, line)
    canvas.save()
    return output.getvalue()


class PdfInputTests(unittest.TestCase):
    def test_pdf_upload_runs_all_four_profiles_and_validates_candidate(self):
        text = (ROOT / 'examples/data_profiles/all_four.txt').read_text(encoding='utf-8')
        extracted = uploaded_text(pdf_bytes(text), 'candidate.pdf')
        report, documents = analyze_text(extracted)
        self.assertEqual(report['export_status'], 'VALID')
        self.assertTrue(all(item['accepted'] for item in report['profiles'].values()))
        self.assertIn('classification Data Architect', documents[0])

    def test_pdf_file_creates_the_same_validated_cli_artifacts(self):
        text = (ROOT / 'examples/data_profiles/full_stack.txt').read_text(encoding='utf-8')
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'resume.pdf'
            source.write_bytes(pdf_bytes(text))
            output = Path(folder) / 'processed'
            report = process_file(source, output, 'full_stack')
            self.assertEqual(report['export_status'], 'VALID')
            self.assertTrue((output / 'candidate.md').exists())
            self.assertEqual(report['source'], 'resume.pdf')

    def test_blank_pdf_and_corrupt_file_are_reported_without_inventing_text(self):
        with self.assertRaisesRegex(ValueError, 'no extractable text'):
            uploaded_text(pdf_bytes(''), 'empty.pdf')
        with self.assertRaisesRegex(ValueError, 'could not be read'):
            uploaded_text(b'not a PDF', 'broken.pdf')

    def test_txt_upload_preserves_utf8_and_rejects_unsupported_formats(self):
        self.assertEqual(uploaded_text('Ana Pérez'.encode('utf-8-sig'), 'resume.txt'), 'Ana Pérez')
        with self.assertRaises(ValueError):
            uploaded_text(b'\xff', 'resume.txt')
        with self.assertRaises(ValueError):
            uploaded_text(b'example', 'resume.docx')


if __name__ == '__main__':
    unittest.main()
