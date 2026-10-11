from pathlib import Path
import xml.etree.ElementTree as ET


def model_tree(resume):
    personal = ("PersonalInfo", [(f"name: {resume.personal.name}", []),
                                  (f"location: {resume.personal.location}", [])])
    contacts = [(f"email: {resume.contact.email}", [])]
    if resume.contact.github:
        contacts.append((f"github: {resume.contact.github}", []))
    jobs = [("Experience", [(f"{field}: {getattr(job, field)}", [])
                            for field in ("position", "company", "years")])
            for job in resume.experiences]
    education = [("Education", [(f"{field}: {getattr(study, field)}", [])
                                for field in ("institution_name", "phone", "program")])
                 for study in resume.educations]
    skills = [(skill.name, []) for skill in resume.skills]
    qualifications = [(f"{q.name} (level {q.level})", []) for q in resume.qualifications]
    classifications = [(c.label, []) for c in resume.classifications]
    return ("Resume", [personal, ("Contact", contacts), ("experiences", jobs),
                       ("educations", education), ("skills", skills),
                       ("qualifications", qualifications),
                       ("classifications", classifications)])


def write_tree_svg(tree, destination):
    nodes = []

    def visit(node, depth, parent):
        label, children = node
        index = len(nodes)
        nodes.append((label, depth, parent))
        for child in children:
            visit(child, depth + 1, index)

    visit(tree, 0, None)
    width = max(700, max(50 + depth * 32 + len(label) * 8 for label, depth, _ in nodes))
    height = 45 + 27 * len(nodes)
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg",
                     width=str(width), height=str(height), viewBox=f"0 0 {width} {height}")
    ET.SubElement(svg, "rect", width="100%", height="100%", fill="white")
    for index, (label, depth, parent) in enumerate(nodes):
        x, y = 24 + depth * 32, 28 + index * 27
        if parent is not None:
            parent_depth = nodes[parent][1]
            parent_x, parent_y = 24 + parent_depth * 32, 28 + parent * 27
            ET.SubElement(svg, "path", d=f"M {parent_x + 4} {parent_y + 6} V {y - 5} H {x - 6}",
                          fill="none", stroke="#a8b2c1")
        element = ET.SubElement(svg, "text", x=str(x), y=str(y), fill="#15263c",
                                attrib={"font-family": "monospace", "font-size": "13"})
        element.text = label
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(svg).write(destination, encoding="utf-8", xml_declaration=True)
