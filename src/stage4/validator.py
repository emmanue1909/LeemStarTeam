import sys
from pathlib import Path
from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError

mm = metamodel_from_file(str(Path(__file__).resolve().parent / "grammar/resume.tx"))


def validate(model):
    errors = []

    records = [(model.personal, ("name", "location")), (model.contact, ("email",))]
    records += [(item, ("position", "company")) for item in model.experiences]
    records += [(item, ("institution_name", "phone", "program")) for item in model.educations]
    records += [(item, ("name",)) for item in [*model.skills, *model.qualifications]]
    for item, fields in records:
        for field in fields:
            if not getattr(item, field).strip():
                errors.append(f"Campo obligatorio vacío: {type(item).__name__}.{field}")

    #Experience.years: no negativo, no mayor a 60
    for exp in model.experiences:
        if exp.years < 0 or exp.years > 60:
            errors.append(f"Años inválidos en experiencia '{exp.position}': {exp.years}")

    #Qualification.level: entre 1 y 5
    for q in model.qualifications:
        if q.level < 1 or q.level > 5:
            errors.append(f"Nivel inválido en qualification '{q.name}': {q.level}")

    #Contact.email: debe contener '@' y un '.' después del '@'
    email = model.contact.email
    if "@" not in email:
        errors.append(f"Email sin '@': {email}")
    else:
        domain = email.split("@", 1)[1]
        if "." not in domain:
            errors.append(f"Email sin dominio válido: {email}")

    #Classification: no repetir el mismo perfil dos veces
    labels = [c.label for c in model.classifications]
    duplicated = {l for l in labels if labels.count(l) > 1}
    if duplicated:
        errors.append(f"Clasificación(es) repetida(s): {', '.join(duplicated)}")

    #Education.phone: debe empezar con '+'
    for edu in model.educations:
        if not edu.phone.startswith("+"):
            errors.append(f"Teléfono sin prefijo '+' en institución '{edu.institution_name}': {edu.phone}")

    #Skill.name: no repetir la misma skill dos veces
    skill_names = [s.name for s in model.skills]
    duplicated_skills = {s for s in skill_names if skill_names.count(s) > 1}
    if duplicated_skills:
        errors.append(f"Skill(s) repetida(s): {', '.join(duplicated_skills)}")

    qualifications = [q.name for q in model.qualifications]
    if len(qualifications) != len(set(qualifications)):
        errors.append("Qualification(s) repetida(s)")

    #Experience.company y Education.institution_name no vacíos
    for exp in model.experiences:
        if not exp.company.strip():
            errors.append(f"Empresa vacía en experiencia '{exp.position}'")
    for edu in model.educations:
        if not edu.institution_name.strip():
            errors.append("Nombre de institución vacío en un registro de educación")

    return errors


def parse_validated(path):
    model = mm.model_from_file(str(path), encoding="utf-8")
    errors = validate(model)
    if errors:
        raise ValueError("Invalid candidate profile: " + "; ".join(errors))
    return model


def main():
    if len(sys.argv) != 2:
        print("Uso: python -m src.stage4.validator <archivo.resume>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        model = mm.model_from_file(file_path)
    except TextXSyntaxError as e:
        print(f"Error de sintaxis en {file_path}: {e}")
        sys.exit(1)

    errors = validate(model)

    if len(errors) != 0:
        print(f"Modelo inválido ({len(errors)} error(es)):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("Modelo válido, todas las reglas de negocio se cumplen.")


if __name__ == "__main__":
    main()
