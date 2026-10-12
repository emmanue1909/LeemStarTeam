"""Build the English research poster from the executable models and fixtures."""
import argparse
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A2, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.data_app import analyze_text
from src.data_profiles import PROFILES
from src.stage3.classify_data import AUTOMATA

ROOT = Path(__file__).resolve().parents[1]


def build_poster(destination, passed_tests):
    width, height = landscape(A2)
    c = Canvas(str(destination), pagesize=(width, height), pageCompression=1)
    c.setTitle('ResumeLens - Formal models for structured resume evidence')
    c.setAuthor('LeemStarTeam')
    c.setCreator('')
    ink, muted, teal = map(HexColor, ('#173047', '#456074', '#087f8c'))
    orange, pale = HexColor('#d67d2c'), HexColor('#edf4f7')
    c.setFillColor(pale)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    margin, gap = 40, 26
    col = (width - 2 * margin - 2 * gap) / 3
    xs = [margin + i * (col + gap) for i in range(3)]
    body = ParagraphStyle('body', fontName='Helvetica', fontSize=21, leading=27, textColor=ink)
    small = ParagraphStyle('small', parent=body, fontSize=18, leading=24)

    def label(x, y, text, size=21, bold=False, color=ink):
        c.setFillColor(color)
        c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
        c.drawString(x, y, text)

    def paragraph(x, top, text, available, style=body):
        p = Paragraph(text, style)
        _, h = p.wrap(available, 2000)
        p.drawOn(c, x, top-h)
        return top-h

    def card(index, top, h, title):
        x = xs[index]
        c.setFillColor(white)
        c.roundRect(x, top-h, col, h, 12, fill=1, stroke=0)
        label(x+22, top-38, title, 26, True, teal)
        return x+22, top-64, col-44

    def arrow(x1, y1, x2, y2, color=teal):
        c.setStrokeColor(color)
        c.setLineWidth(2)
        c.line(x1, y1, x2, y2)
        import math
        angle = math.atan2(y2-y1, x2-x1)
        p = c.beginPath()
        p.moveTo(x2, y2)
        for offset in (-0.45, 0.45):
            p.lineTo(x2-10*math.cos(angle+offset), y2-10*math.sin(angle+offset))
        p.close()
        c.setFillColor(color)
        c.drawPath(p, fill=1, stroke=0)

    label(margin, height-82, 'ResumeLens', 61, True)
    label(margin, height-127, 'Formal models for structured resume evidence', 29)
    label(margin, height-161, 'LeemStarTeam | Discrete Structures III | Integrative Task 1', 18, color=muted)
    label(margin, height-199, 'Can formal models normalize aliases and recognize several qualification patterns?', 24, True)

    boxw = (width-2*margin-3*35)/4
    for i, (name, caption) in enumerate([
            ('EXTRACT', 'Regex: raw terms and records'),
            ('NORMALIZE', 'FST: aliases to canonical tokens'),
            ('RECOGNIZE', 'DFA: independent profile patterns'),
            ('VALIDATE', 'textX + rules -> Markdown')]):
        x, top = margin+i*(boxw+35), height-222
        c.setFillColor(teal)
        c.roundRect(x, top-63, boxw, 63, 9, fill=1, stroke=0)
        label(x+15, top-26, str(i+1)+'  '+name, 21, True, white)
        label(x+15, top-49, caption, 16, color=white)
        if i < 3:
            arrow(x+boxw+5, top-31, x+boxw+30, top-31)

    top = height-307
    x, y, w = card(0, top, 231, 'Problem and method')
    y = paragraph(x, y, 'Aliases can describe the same technology. '
        'Candidates may fit several profiles.', w)
    y = paragraph(x, y-16, 'We separate evidence, normalization, recognition '
        'and validation using formal models.', w)
    assert y >= top-218

    x, y, w = card(0, top-250, 508, 'Models and profile languages')
    y = paragraph(x, y, '<b>FST:</b> (Q, Sigma, Gamma, delta, omega, q0, F). '
        'Complete aliases are input symbols; canonical terms are output symbols.', w, small)
    y = paragraph(x, y-12, '<b>DFA:</b> (Q, Sigma, delta, q0, F). '
        'One target per state/symbol; no epsilon transitions.', w, small)
    table_top = y-26
    label(x, table_top, 'Profile', 18, True)
    label(x+235, table_top, 'States', 18, True)
    label(x+335, table_top, 'Policy', 18, True)
    rows = [('machine_learning', 'ML Engineer', 'Ordered'),
            ('data_architect', 'Data Architect', 'Ordered'),
            ('full_stack', 'Full Stack', 'Coverage'),
            ('cybersecurity', 'Cybersecurity', 'Coverage')]
    for i, (key, title, policy) in enumerate(rows):
        rowy = table_top-30*(i+1)
        label(x, rowy, title, 19)
        label(x+254, rowy, str(len(AUTOMATA[key].states)), 21, True)
        label(x+335, rowy, policy, 19)
    y = paragraph(x, table_top-152, 'ML/Data Architect use sorted category tokens. '
        'Full Stack/Cybersecurity remember covered categories.', w, small)
    y = paragraph(x, y-12, 'AND across required categories; OR among alternatives. '
        'Retain every satisfied profile.', w, small)
    assert y >= top-745

    x, y, w = card(1, top, 309, 'Alias translation: actual FST')
    paragraph(x, y, 'Postgres is extracted unchanged. Lexical preparation supplies '
        'the atomic symbol <b>postgres</b> to the shared skill FST.', w)
    cy = top-179
    c.setStrokeColor(teal)
    c.setLineWidth(2)
    for cx, name in ((x+65, 'q0'), (x+380, 'q1')):
        c.circle(cx, cy, 27, fill=0, stroke=1)
        if name == 'q1':
            c.circle(cx, cy, 22, fill=0, stroke=1)
        label(cx-14, cy-7, name, 23, True)
    arrow(x+1, cy, x+34, cy)
    arrow(x+95, cy, x+350, cy)
    label(x+113, cy+20, 'postgres : POSTGRESQL', 18, True)
    label(x+35, cy-53, 'input alias', 18, color=muted)
    label(x+297, cy-53, 'accepting state', 18, color=muted)
    paragraph(x, top-253, 'The API emits [POSTGRESQL]. Reset q0 for each term. '
        'Unknown aliases have no translation.', w, small)

    x, y, w = card(1, top-328, 430, 'ML: accepted and rejected traces')
    tokens = ['PYTHON', 'PANDAS', 'TENSORFLOW', 'POSTGRESQL', 'GIT']
    cy = top-451
    step = (w-40)/5
    for i in range(6):
        cx = x+20+i*step
        c.setStrokeColor(teal)
        c.setLineWidth(2)
        c.circle(cx, cy, 22, fill=0, stroke=1)
        if i == 5:
            c.circle(cx, cy, 17, fill=0, stroke=1)
        label(cx-12, cy-6, 'q'+str(i), 18, True)
        if i < 5:
            arrow(cx+24, cy, cx+step-25, cy)
            label(cx+step/2-8, cy+28, 'C'+str(i+1), 15, True)
    for i, token in enumerate(tokens):
        rowy = cy-58-i*32
        label(x+4, rowy, 'C'+str(i+1), 18, True, teal)
        label(x+48, rowy, token, 19)
        label(x+300, rowy, 'q'+str(i)+' -> q'+str(i+1), 18)
    label(x+4, cy-227, 'All five categories: q5 -> ACCEPTED', 20, True, teal)
    label(x+4, cy-264, 'Without Git: q4 -> REJECTED', 20, True, orange)
    paragraph(x, cy-270, 'Sorting makes resume order independent.', w, small)

    x, y, w = card(2, top, 353, 'Measured verification results')
    label(x, y-21, str(passed_tests), 60, True, teal)
    label(x+132, y-5, 'tests passed', 26, True)
    label(x+132, y-32, '98 unittest + 142 function cases', 16, color=muted)
    fixture_names = ['ml_engineer', 'data_architect', 'ml_english', 'architect_english',
                     'ml_and_architect', 'full_stack', 'cybersecurity', 'all_four']
    for name in fixture_names:
        report, docs = analyze_text((ROOT / f'examples/data_profiles/{name}.txt').read_text(encoding='utf-8'))
        assert report['export_status'] == 'VALID' and docs
    incomplete = ['ml_incomplete', 'data_architect_incomplete', 'full_stack_incomplete', 'cybersecurity_incomplete']
    for name in incomplete:
        report, docs = analyze_text((ROOT / f'examples/data_profiles/{name}.txt').read_text(encoding='utf-8'))
        assert report['export_status'] == 'NOT_ACCEPTED' and docs is None
    bars = [('Valid candidate exports', len(fixture_names), teal),
            ('Incomplete patterns rejected', len(incomplete), orange)]
    for i, (title, count, color) in enumerate(bars):
        by = top-179-i*64
        label(x, by+5, title, 18, True)
        c.setFillColor(pale)
        c.roundRect(x, by-26, w-55, 17, 5, fill=1, stroke=0)
        c.setFillColor(color)
        c.roundRect(x, by-26, (w-55)*count/8, 17, 5, fill=1, stroke=0)
        label(x+w-42, by-27, str(count), 25, True, color)
    paragraph(x, top-286, 'Checks compare model tables and cover aliases, missing '
        'categories, boundaries, PDF input and UI state.', w, small)

    x, y, w = card(2, top-372, 386, 'Conclusion and limits')
    y = paragraph(x, y, '<b>Conclusion:</b> models give reproducible normalization '
        'and multi-profile recognition within the declared input language.', w, small)
    y = paragraph(x, y-15, '<b>Acceptance is not exportability.</b> Missing records '
        'or explicit area levels can block the candidate\'s export.', w, small)
    y = paragraph(x, y-15, 'Regex does not interpret negation or verify claims. '
        'Scanned PDFs require OCR outside this project.', w, small)
    y = paragraph(x, y-15, 'No real-world hiring accuracy was measured. Categories '
        'and bounds are team policies, not professional standards.', w, small)
    assert y >= top-746

    label(margin, 87, 'References and reproducibility', 17, True, muted)
    label(margin, 62, 'Romero (2021), Pyformlang. DOI: 10.1145/3408877.3432464', 15, color=muted)
    label(margin, 40, 'Dejanovic et al. (2017), TextX. DOI: 10.1016/j.knosys.2016.10.023', 15, color=muted)
    label(xs[2], 62, 'Published models + fictional fixtures + test suite', 15, color=muted)
    label(xs[2], 40, 'github.com/emmanue1909/LeemStarTeam', 15, color=muted)
    c.save()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--passed-tests', required=True, type=int)
    args = parser.parse_args()
    if args.passed_tests != 240:
        parser.error('Review the poster case breakdown if the verified test count changes.')
    destination = ROOT / 'output/pdf/ResumeLens_Poster_English.pdf'
    destination.parent.mkdir(parents=True, exist_ok=True)
    build_poster(destination, args.passed_tests)
    print(destination)


if __name__ == '__main__':
    main()
