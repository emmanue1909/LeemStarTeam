import re
import xml.etree.ElementTree as ET
from pathlib import Path

from src.data_profiles import PROFILES, lexical_token, vocabulary
from src.stage2.normalize_data import TRANSDUCERS
from src.stage3.classify_data import AUTOMATA, next_state

ROOT = Path(__file__).resolve().parents[1]


def draw_transducer(profile, destination):
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
    for x, label in ((70, "q0"), (1020, "q1")):
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
        text.text = " | ".join(sorted({lexical_token(x) for x in aliases})) + " / " + canonical
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
    print("Wrote both formal definitions, complete matrices and FST/DFA diagrams.")


if __name__ == "__main__":
    main()
