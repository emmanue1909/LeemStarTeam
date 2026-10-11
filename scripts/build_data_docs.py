import re
import xml.etree.ElementTree as ET
from pathlib import Path

from src.data_profiles import PROFILES, SKILL_VARIANTS, QUALIFICATION_VARIANTS, lexical_token, vocabulary
from src.stage2.normalize_data import TRANSDUCERS, SKILL_TRANSDUCER, QUALIFICATION_TRANSDUCER
from src.stage3.classify_data import AUTOMATA, EMMANUEL_AUTOMATA, next_state, state_coverage
from src.emmanuel_bridge import NORMALIZER

ROOT = Path(__file__).resolve().parents[1]


def draw_transducer(profile, destination, input_transform=lexical_token, final_state="q1"):
    spec = PROFILES[profile]
    rows = list(spec["variants"].items())
    height = 130 + 48 * len(rows)
    center = height // 2
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width="1100", height=str(height))
    ET.SubElement(svg, "rect", width="100%", height="100%", fill="white")
    title = ET.SubElement(svg, "text", x="25", y="28", attrib={"font-family": "Arial", "font-size": "20"})
    title.text = spec["label"] + " normalization FST"
    ET.SubElement(svg, "path", d=f"M 10 {center} H 44", stroke="black")
    ET.SubElement(svg, "polygon", points=f"44,{center} 35,{center-5} 35,{center+5}", fill="black")
    for x, label in ((70, "q0"), (1020, final_state)):
        ET.SubElement(svg, "circle", cx=str(x), cy=str(center), r="26", fill="white", stroke="black")
        text = ET.SubElement(svg, "text", x=str(x - 10), y=str(center + 5), attrib={"font-family": "Arial", "font-size": "14"})
        text.text = label
    ET.SubElement(svg, "circle", cx="1020", cy=str(center), r="21", fill="none", stroke="black")
    for i, (canonical, aliases) in enumerate(rows):
        y = 72 + i * 48
        ET.SubElement(svg, "path", d=f"M 96 {center} Q 130 {y} 180 {y} H 900 Q 960 {y} 994 {center}",
                      fill="none", stroke="#668096")
        ET.SubElement(svg, "polygon", points=f"994,{center} 984,{center-5} 984,{center+5}", fill="#668096")
        text = ET.SubElement(svg, "text", x="190", y=str(y - 7), attrib={"font-family": "Arial", "font-size": "12"})
        text.text = " | ".join(sorted({input_transform(x) for x in aliases})) + " / " + canonical
    note = ET.SubElement(svg, "text", x="25", y=str(height - 20), attrib={"font-family": "Arial", "font-size": "13"})
    note.text = "Each alias separated by | is a separate input symbol/transition; / separates input and output. No other transitions."
    ET.ElementTree(svg).write(destination, encoding="utf-8", xml_declaration=True)


def draw_automaton(profile, destination):
    k = len(PROFILES[profile]["categories"])
    height = 190 + k * 90
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width="800", height=str(height), viewBox=f"0 0 800 {height}")
    ET.SubElement(svg, "rect", width="100%", height="100%", fill="white")

    def text(x, y, value, size=14):
        node = ET.SubElement(svg, "text", x=str(x), y=str(y), fill="#142536", attrib={"font-family": "Arial", "font-size": str(size)})
        node.text = value

    def arrow(x1, y1, x2, y2):
        ET.SubElement(svg, "line", x1=str(x1), y1=str(y1), x2=str(x2), y2=str(y2), stroke="#24384a", attrib={"stroke-width": "1.5"})
        if x1 == x2:
            points = f"{x2},{y2} {x2 - 5},{y2 - 9} {x2 + 5},{y2 - 9}"
        else:
            points = f"{x2},{y2} {x2 - 9},{y2 - 5} {x2 - 9},{y2 + 5}"
        ET.SubElement(svg, "polygon", points=points, fill="#24384a")

    text(25, 27, PROFILES[profile]["label"], 20)
    arrow(30, 70, 85, 70)
    for i in range(k + 1):
        y = 70 + i * 90
        ET.SubElement(svg, "circle", cx="110", cy=str(y), r="25", fill="white", stroke="#24384a", attrib={"stroke-width": "2"})
        text(101, y + 5, f"q{i}")
        if i == k:
            ET.SubElement(svg, "circle", cx="110", cy=str(y), r="20", fill="none", stroke="#24384a")
        if i < k:
            arrow(110, y + 25, 110, y + 65)
            name, tokens = PROFILES[profile]["categories"][i]
            text(153, y + 48, f"C{i + 1}: {name}")
            text(153, y + 67, ", ".join(tokens), 12)
        if i:
            ET.SubElement(svg, "path", d=f"M 90 {y-15} C 30 {y-50}, 30 {y+50}, 90 {y+15}", fill="none", stroke="#24384a")
            ET.SubElement(svg, "polygon", points=f"90,{y+15} 80,{y+9} 83,{y+20}", fill="#24384a")
            text(25, y + 5, f"C{i}", 12)
    dead_y = height - 65
    ET.SubElement(svg, "circle", cx="350", cy=str(dead_y), r="30", fill="white", stroke="#24384a")
    text(328, dead_y + 5, "q_dead", 12)
    ET.SubElement(svg, "path", d=f"M 330 {dead_y-22} C 270 {dead_y-70}, 420 {dead_y-70}, 370 {dead_y-22}", fill="none", stroke="#24384a")
    ET.SubElement(svg, "polygon", points=f"370,{dead_y-22} 371,{dead_y-33} 361,{dead_y-29}", fill="#24384a")
    text(330, dead_y - 58, "Sigma", 12)
    text(400, dead_y - 12, "Every other transition goes to q_dead.", 13)
    text(400, dead_y + 10, "Exact targets appear in the full transition table.", 13)
    text(25, height - 12, "Ci denotes the token set shown on the advancing edge. Input is in canonical category order.", 12)
    ET.ElementTree(svg).write(destination, encoding="utf-8", xml_declaration=True)


def main():
    folder = ROOT / "docs/data_profiles"
    diagrams = folder / "diagrams"
    diagrams.mkdir(parents=True, exist_ok=True)
    for profile, spec in PROFILES.items():
        if profile in EMMANUEL_AUTOMATA:
            coverage_documents(profile, folder, diagrams)
            continue
        words = vocabulary(profile)
        k = len(spec["categories"])
        states = [f"q{i}" for i in range(k + 1)] + ["q_dead"]
        lines = [f'# {spec["label"]} formal models', "", "## Stage 1 qualification expressions", "",
                 "All expressions use `re.IGNORECASE`. The extractor returns the original matched text.", "",
                 "| Term | Recognized aliases |", "|---|---|"]
        expressions = []
        for token in words:
            parts = [re.escape(x).replace(r"\ ", r"\s+") for x in sorted(spec["variants"][token], key=len, reverse=True)]
            expression = r"(?<!\w)(?:" + "|".join(parts) + r")(?!\w)"
            lines.append(f"| {token} | " + ", ".join(spec["variants"][token]) + " |")
            expressions.append(f"{token}: {expression}")
        lines += ["", "Exact expressions:", "", "```text", *expressions, "```"]
        lines += ["", "## Stage 2 finite state transducer", "", "M = (Q, Sigma, Gamma, delta, omega, q0, F).", "",
                  "- Q = {q0, q1}; q0 is initial and F = {q1}.",
                  "- Sigma is the finite set of input tokens in the table below; each complete alias is one atomic symbol.",
                  "- Gamma = {" + ", ".join(words) + "}.",
                  "- For each table row (x, y): delta(q0, x) = q1 and omega(q0, x) = [y]. All other transitions are absent.",
                  "- The FST processes one extracted term at a time; it is reset between terms. An unknown term has no translation.",
                  "- Before translation, `casefold` and whitespace squeezing only unify the lexical representation. Alias equivalence is performed by the FST.",
                  "", "| Input token x | Output token y | delta | omega |", "|---|---|---|---|"]
        for token in words:
            for alias in sorted({lexical_token(x) for x in spec["variants"][token]}):
                lines.append(f"| `{alias}` | `{token}` | q0 to q1 | [{token}] |")
        lines += ["", f"![FST diagram](diagrams/{profile}_fst.svg)", "", f"[Complete FST transition graph](diagrams/{profile}_fst.dot)", "",
                  "## Stage 3 deterministic finite automaton", "", "M = (Q, Sigma, delta, q0, F).", "",
                  "- Q = {" + ", ".join(states) + "}.", "- Sigma = {" + ", ".join(words) + "}.",
                  f"- Initial state: q0. F = {{q{k}}}.",
                  "- delta is defined for every state and every symbol by the matrix below; q_dead is a nonaccepting sink.",
                  "- qi records that the first i categories have been satisfied. Repeated alternatives in the current category keep the same state.",
                  "- A skipped, decreasing or unknown category is rejected. The pipeline sorts and deduplicates first, so the résumé's original order does not affect the result.",
                  "- There is exactly one destination per state/symbol pair and no epsilon transition: this is a DFA.",
                  "", "The language is L = C1+ C2+ ... Ck+. Within each Ci, alternatives are OR; across categories, requirements are AND.", "",
                  "| Category | Required evidence |", "|---|---|"]
        for i, (name, tokens) in enumerate(spec["categories"], 1):
            lines.append(f"| C{i}: {name} | " + " or ".join(tokens) + " |")
        lines += ["", f"![DFA diagram](diagrams/{profile}_dfa.svg)", "", f"[All DFA edges in DOT format](diagrams/{profile}_dfa.dot)", "",
                  "## Full transition matrix", "", "An arrow marks the initial state; * marks the accepting state.", "",
                  "| State | " + " | ".join(words) + " |", "|---|" + "---|" * len(words)]
        for state in states:
            label = ("-> " if state == "q0" else "* " if state == f"q{k}" else "") + state
            lines.append("| " + label + " | " + " | ".join(next_state(state, token, profile) for token in words) + " |")
        lines += ["", "## Limitations", "", "The model recognizes explicitly named qualifications under the proposed category policy. It does not rank candidates, infer proficiency, handle negated claims or verify experience. Unrecognized résumé terms do not satisfy a required category.", ""]
        (folder / f"{profile}.md").write_text("\n".join(lines), encoding="utf-8")
        TRANSDUCERS[profile].write_as_dot(str(diagrams / f"{profile}_fst.dot"))
        AUTOMATA[profile].write_as_dot(str(diagrams / f"{profile}_dfa.dot"))
        draw_transducer(profile, diagrams / f"{profile}_fst.svg")
        draw_automaton(profile, diagrams / f"{profile}_dfa.svg")
    shared_transducer_documents(folder, diagrams)
    print('Wrote four formal definitions, complete matrices, FST/DFA diagrams and the shared normalization contract.')


def coverage_documents(profile, folder, diagrams):
    spec, dfa = PROFILES[profile], AUTOMATA[profile]
    states = sorted((str(s.value) for s in dfa.states), key=lambda value: int(value[1:]))
    alphabet = sorted(str(s.value) for s in dfa.symbols)
    areas = [name.upper() for name, _ in spec['categories']]
    coverage = state_coverage(profile)
    final = str(next(iter(dfa.final_states)).value)
    lines = [f'# {spec["label"]}: formal models', '',
             'The subset construction preserves Emmanuel\'s published classifier at `4a102a7`.',
             'The adapter preserves its coverage policy and sequential state names, and maps the shared technology alphabet to the published symbols.',
             '', '## Stage 1 skill expressions', '', '| Term | Recognized aliases |', '|---|---|']
    for token, aliases in spec['variants'].items():
        lines.append(f'| {token} | ' + ', '.join(aliases) + ' |')
    lines += ['', 'Regex construction and shared FST definitions: [shared models](shared_models.md).', '',
              '## Stage 2 profile vocabulary projection', '',
              'All profiles use the same skill FST. PostgreSQL and MySQL remain distinct in the DSL; the classifier treats them as database evidence.',
              'The profile-specific alias table below is also implemented as a pyformlang FST for direct compatibility calls.',
              '', '| Input token x | Output token y | delta | omega |', '|---|---|---|---|']
    for token, aliases in spec['variants'].items():
        for alias in sorted({lexical_token(a) for a in aliases}):
            lines.append(f'| `{alias}` | `{token}` | q0 to q1 | [{token}] |')
    TRANSDUCERS[profile].write_as_dot(str(diagrams / f'{profile}_fst.dot'))
    draw_transducer(profile, diagrams / f'{profile}_fst.svg')
    lines += ['', f'![FST](diagrams/{profile}_fst.svg)', '', '## Stage 3 DFA: complete 5-tuple', '',
              'M = (Q, Sigma, delta, q0, F).', '', '- Q = {' + ', '.join(states) + '}.',
              '- Sigma = {' + ', '.join(alphabet) + '}.', '- q0 = q0 (empty coverage).',
              '- F = {' + final + '} (all required categories covered).',
              '- State qN follows the contributor\'s sequential enumeration by coverage size. The coverage table below specifies its meaning.',
              '- delta adds the category evidenced by a skill, or keeps the state for an already covered category or a known irrelevant skill.',
              '- The complete transition function is the executable-model matrix below. Unknown symbols outside Sigma have no transition and are rejected.',
              '- One target per state/symbol pair and no epsilon transitions make this a DFA.',
              '- AND across required categories; OR among alternatives. The order and duplicates do not affect coverage.',
              '- CEH, OSCP and Security+ are optional skills, not requirements.', '', '| Category index | Area |', '|---|---|']
    lines += [f'| {i} | {area} |' for i, area in enumerate(areas)]
    lines += ['', '| State | Covered categories |', '|---|---|']
    lines += ['| ' + state + ' | ' + (', '.join(areas[i] for i in coverage[state]) or '(none)') + ' |' for state in states]
    lines += ['', '| Required category | Alternative evidence |', '|---|---|']
    lines += ['| ' + name + ' | ' + ' or '.join(tokens) + ' |' for name, tokens in spec['categories']]
    lines += ['', f'![Coverage DFA](diagrams/{profile}_dfa.svg)', '',
              f'[All DFA transitions](diagrams/{profile}_dfa.dot)', '', '## Full transition matrix', '',
              '| State | ' + ' | '.join(alphabet) + ' |', '|---|' + '---|' * len(alphabet)]
    for state in states:
        label = ('-> ' if state == 'q0' else '* ' if state == final else '') + state
        lines.append('| ' + label + ' | ' + ' | '.join(str(dfa(state, token)[0].value) for token in alphabet) + ' |')
    (folder / f'{profile}.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    dfa.write_as_dot(str(diagrams / f'{profile}_dfa.dot'))
    draw_coverage(profile, diagrams / f'{profile}_dfa.svg', areas)


def draw_coverage(profile, destination, areas):
    """Draw each subset state and every advancing category edge; loops are summarized."""
    count = len(areas)
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width='1500', height='1100', viewBox='0 0 1500 1100')
    ET.SubElement(svg, 'rect', width='100%', height='100%', fill='white')
    colors = ['#0072B2', '#B57100', '#009E73', '#9D4F8E', '#D55E00']
    def label(x, y, value, size=13, color='#142536'):
        node = ET.SubElement(svg, 'text', x=str(x), y=str(y), fill=color, attrib={'font-family': 'Arial', 'font-size': str(size)})
        node.text = value
    label(20, 30, PROFILES[profile]['label'] + ' — subset coverage DFA', 21)
    positions = {}
    coverage = state_coverage(profile)
    labels = {sum(1 << i for i in indices): state for state, indices in coverage.items()}
    for depth in range(count + 1):
        masks = [n for n in range(1 << count) if n.bit_count() == depth]
        for index, mask in enumerate(masks):
            positions[mask] = (65 + depth * 250, 125 + (index + 0.5) * 740 / len(masks))
    for mask, (x, y) in positions.items():
        for bit in range(count):
            if mask & (1 << bit):
                continue
            tx, ty = positions[mask | (1 << bit)]
            ET.SubElement(svg, 'line', x1=str(x + 20), y1=str(y), x2=str(tx - 20), y2=str(ty),
                          stroke=colors[bit], attrib={'stroke-width': '1.6', 'data-category': str(bit)})
            ET.SubElement(svg, 'polygon', points=f'{tx-20},{ty} {tx-28},{ty-4} {tx-28},{ty+4}', fill=colors[bit])
    for mask, (x, y) in positions.items():
        ET.SubElement(svg, 'circle', cx=str(x), cy=str(y), r='21', fill='white', stroke='#234459')
        if mask == (1 << count) - 1:
            ET.SubElement(svg, 'circle', cx=str(x), cy=str(y), r='17', fill='none', stroke='#234459')
        label(x - 13, y + 4, labels[mask], 12)
    x, y = positions[0]
    ET.SubElement(svg, 'line', x1='12', y1=str(y), x2=str(x - 22), y2=str(y), stroke='black')
    ET.SubElement(svg, 'polygon', points=f'{x-22},{y} {x-30},{y-5} {x-30},{y+5}', fill='black')
    for index, area in enumerate(areas):
        label(25, 910 + index * 23, f'C{index+1}: {area}', 15, colors[index])
    label(25, 1038, 'Arrow colors identify the category added to the coverage set; states are arranged by number of covered categories.')
    label(25, 1060, 'All states loop on already covered categories and known irrelevant skills. The full transition matrix includes every loop.')
    ET.ElementTree(svg).write(destination, encoding='utf-8', xml_declaration=True)


def shared_transducer_documents(folder, diagrams):
    lines = ['# Shared extraction and normalization models', '',
             'All four profiles use these two separate pyformlang FSTs. Competence names and technologies occupy different namespaces.',
             'No FST transforms personal names, years, or proficiency levels. Levels are explicitly extracted integers.', '',
             '## Extraction expressions', '',
             'A combined regex orders escaped aliases longest first; it squeezes variable whitespace with `\\s+` and uses `(?<!\\w)` / `(?!\\w)` boundaries.',
             'Stage 1 preserves the matched spelling. Contact URLs/email and explicit area-level declarations are masked before matching technology claims.',
             'Names accept Unicode first-line names or `mi nombre es` / `my name is`. Anchors take priority.',
             'Experiences accept semicolon/period followed by `tengo N años de experiencia` or `mi experiencia es de N años`; repeated records retain their own years.', '',
             'Exact regex constants are in [the extractor](../../src/stage1/extract_data.py).', '']
    for name, variants, fst in [('shared_skills', SKILL_VARIANTS, SKILL_TRANSDUCER),
                                ('shared_qualifications', QUALIFICATION_VARIANTS, QUALIFICATION_TRANSDUCER)]:
        lines += ['## ' + name, '', 'M = (Q, Sigma, Gamma, delta, omega, q0, F).', '',
                  '- Q = {q0, q1}; initial q0; F = {q1}.',
                  '- Sigma = the complete input column below, each alias an atomic symbol.',
                  '- Gamma = {' + ', '.join(variants) + '}.',
                  '- Each row defines delta(q0, alias) = q1 and omega(q0, alias) = [canonical]. No other transitions.',
                  '- casefold and whitespace squeezing prepare the input; equivalence is performed by the FST.',
                  '- Reset per term; unknown terms have no accepting path. Deduplication is performed after translation.', '',
                  '| Input | Output | delta | omega |', '|---|---|---|---|']
        for token, aliases in variants.items():
            for alias in sorted({lexical_token(a) for a in aliases}):
                lines.append(f'| `{alias}` | `{token}` | q0 -> q1 | [{token}] |')
        fst.write_as_dot(str(diagrams / f'{name}_fst.dot'))
        # Reuse the same rendering function with a temporary drawing configuration.
        PROFILES[name] = {'label': name, 'variants': variants}
        try:
            draw_transducer(name, diagrams / f'{name}_fst.svg')
        finally:
            del PROFILES[name]
        lines += ['', f'![FST](diagrams/{name}_fst.svg)', '', f'[Complete transitions](diagrams/{name}_fst.dot)', '']
    name = 'published_team_normalizer'
    variants = NORMALIZER.tabla_variantes
    lines += ['## ' + name, '',
              "Full Stack and Cybersecurity also execute Emmanuel's unchanged global normalizer from `4a102a7`.",
              'It combines the native skill and area aliases in a single FST. The adapter maps its outputs to the shared contract and checks them against extracted evidence.', '',
              'M = (Q, Sigma, Gamma, delta, omega, q0, F).', '',
              '- Q = {q0, qf}; initial q0; F = {qf}.',
              '- Sigma is exactly the input column below; complete uppercase aliases are atomic symbols.',
              '- Gamma = {' + ', '.join(variants) + '}.',
              '- Each row defines delta(q0, alias) = qf and omega(q0, alias) = [canonical]. No other transitions.',
              '- The published normalizar function applies upper() before translation; reset per extracted term.',
              '- Qualifications retain their separately extracted level in (level, canonical area) tuples.', '',
              '| Input | Output | delta | omega |', '|---|---|---|---|']
    for token, aliases in variants.items():
        for alias in sorted({a.upper() for a in aliases}):
            lines.append(f'| `{alias}` | `{token}` | q0 -> qf | [{token}] |')
    NORMALIZER.fst_global.write_as_dot(str(diagrams / f'{name}_fst.dot'))
    PROFILES[name] = {'label': 'Published team normalizer', 'variants': variants}
    try:
        draw_transducer(name, diagrams / f'{name}_fst.svg', input_transform=str.upper, final_state='qf')
    finally:
        del PROFILES[name]
    lines += ['', f'![FST](diagrams/{name}_fst.svg)', '', f'[Complete transitions](diagrams/{name}_fst.dot)', '']
    (folder / 'shared_models.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == "__main__":
    main()
