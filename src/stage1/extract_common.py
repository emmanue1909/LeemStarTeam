import re


def extract_email(text):
    pattern = re.compile(r"([a-z]|[A-Z]|\d|\.|_)([a-z]|[A-Z]|\d|\.|_)*@{1}([A-Z]|[a-z]|\d|_)+(\.{1}(\w+))+")
    match = pattern.search(text)
    if match:
        return match.group(0)
    else:
        return None


def extract_phone(text):
    pattern = re.compile(r"\+(\d){2}-\d-(\d){7}(?!\d)")
    match = pattern.search(text)
    if match:
        return match.group(0)
    else:
        return None


def extract_experience_years(text):
    pattern = re.compile(r"[Mm]i experiencia es de ([1-5]\d|[1-9]) años")
    match = pattern.search(text)
    if match:
        return match.group(1)
    else:
        return None


def extract_name(text):
    pattern = re.compile(r"mi nombre es ([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b(?!\s[A-Z])")
    match = pattern.search(text)
    if match:
        return match.group(1)
    else:
        return None

def extract_location(text):
    pattern = re.compile(r"radicad[oa] en ([^.]+)")
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def extract_github(text):
    pattern = re.compile(r"usuario de GitHub es ([A-Za-z0-9-]+)")
    match = pattern.search(text)
    if match:
        return match.group(1)
    else:
        return None

def extract_position_company(text):
    pattern = re.compile(r"posición es (.+?) en la compañía ([^.]+)")
    match = pattern.search(text)
    if not match:
        return None, None
    return match.group(1).strip(), match.group(2).strip()


def extract_institution_program(text):
    pattern = re.compile(r"egresad[oa] del programa de (.+?) de la ([^.]+)")
    match = pattern.search(text)
    if not match:
        return None, None
    return match.group(1).strip(), match.group(2).strip()