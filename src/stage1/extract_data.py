import re

from src.data_profiles import PROFILES

EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+"
PHONE = r"\+\d{1,3}-\d{1,4}-\d{4,10}"
NAME = r"[^\W\d_]+(?:[-'][^\W\d_]+)*(?:[ \t]+[^\W\d_]+(?:[-'][^\W\d_]+)*){1,3}"
LOCATION = r"(?:radicad[oa]\s+en|based in|ubicaci[oó]n:)\s+([^\n.;]+)"
GITHUB = r"(?:usuario de GitHub es|GitHub:)\s+([\w-]+)"
EXPERIENCE = (
    r"(?:mi posici[oó]n es|my position is)\s+([^\n;]+?)\s+"
    r"(?:en la compa[nñ][ií]a|at(?: the company)?)\s+([^\n;]+);"
    r"\s*(?:tengo|I have)\s+(\d+)\s+(?:a[nñ]os? de experiencia|years? of experience)"
)
EDUCATION = (
    r"(?:egresad[oa] del programa de|graduate of the program)\s+([^\n;]+?)\s+"
    r"(?:de la|at)\s+([^\n;]+);"
    r"\s*(?:tel[eé]fono institucional|institution phone)\s+(" + PHONE + r")"
)
EXPERIENCE_MENTION = r"\b\d+\s+(?:years? of experience|a[nñ]os? de experiencia)[^\n.]*"
LEVEL = r"([^\n,;:]+?)\s*\(\s*(?:level|nivel)\s+(\d+)\s*\)"


def qualification_pattern(profile):
    aliases = [alias for values in PROFILES[profile]["variants"].values() for alias in values]
    parts = [re.escape(alias).replace(r"\ ", r"\s+") for alias in sorted(set(aliases), key=len, reverse=True)]
    return re.compile(r"(?<!\w)(?:" + "|".join(parts) + r")(?!\w)", re.IGNORECASE)


def extract_qualifications(text, profile):
    text = re.sub(EMAIL + r"|https?://\S+", " ", text, flags=re.IGNORECASE)
    return [match.group() for match in qualification_pattern(profile).finditer(text)]


def extract(text, profile):
    def first(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    email = re.search(EMAIL, text)
    return {
        "name": first_line if re.fullmatch(NAME, first_line) else None,
        "location": first(LOCATION),
        "email": email.group() if email else None,
        "github": first(GITHUB),
        "experiences": [
            {"position": m.group(1).strip(), "company": m.group(2).strip(), "years": int(m.group(3))}
            for m in re.finditer(EXPERIENCE, text, re.IGNORECASE)
        ],
        "experience_mentions": [m.group().strip() for m in re.finditer(EXPERIENCE_MENTION, text, re.IGNORECASE)],
        "educations": [
            {"program": m.group(1).strip(), "institution": m.group(2).strip(), "phone": m.group(3)}
            for m in re.finditer(EDUCATION, text, re.IGNORECASE)
        ],
        "raw_qualifications": extract_qualifications(text, profile),
        "declared_levels": [
            {"term": m.group(1).strip(), "level": int(m.group(2))}
            for m in re.finditer(LEVEL, text, re.IGNORECASE)
        ],
    }
