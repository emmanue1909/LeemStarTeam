import argparse
from pathlib import Path

from textx import metamodel_from_file

GRAMMAR_PATH = Path(__file__).resolve().parents[1] / "grammar" / "resume.tx"


def parse_file(path):
    mm = metamodel_from_file(str(GRAMMAR_PATH))
    return mm.model_from_file(str(path), encoding="utf-8")


def render_markdown(resume):
    labels = ", ".join(c.label for c in resume.classifications)
    lines = [f"# {resume.personal.name}", "", "## Candidate Profile", "",
             f"**Classification:** {labels}", "",
             "## Contact", "", f"- Location: {resume.personal.location}",
             f"- Email: {resume.contact.email}"]
    if resume.contact.github:
        lines.append(f"- GitHub: {resume.contact.github}")

    lines += ["", "## Skills", ""]
    lines += [f"- {skill.name}" for skill in resume.skills]

    lines += ["", "## Qualifications", ""]
    lines += [f"- {q.name} (level {q.level})" for q in resume.qualifications]

    lines += ["", "## Experience", ""]
    for job in resume.experiences:
        lines += [f"### {job.position}", "", f"**{job.company}** — {job.years} year(s)", ""]

    lines += ["## Education", ""]
    for study in resume.educations:
        lines += [f"**{study.institution_name}**", "", f"{study.program}", ""]

    return "\n".join(lines).strip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown from a .resume file")
    parser.add_argument("resume_file")
    parser.add_argument("--output")
    args = parser.parse_args()

    resume = parse_file(args.resume_file)
    markdown = render_markdown(resume)

    output_path = Path(args.output) if args.output else Path("output") / (Path(args.resume_file).stem + ".md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
