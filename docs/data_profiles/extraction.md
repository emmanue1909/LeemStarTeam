# Shared extraction

The extractor uses Python `re` and preserves original spelling. Exact constants and composed regexes appear in `src/stage1/extract_data.py` and [shared model documentation](shared_models.md).

Names use `mi nombre es Ana Pérez.` / `My name is Mary Jane Watson.`; a standalone first-line name remains supported. Unicode letters, apostrophes and hyphens are supported within the documented 2–4-word bound. An explicit anchor has priority.

Common records support both formats:

```text
Mi posición es Engineer en la compañía Andes; tengo 3 años de experiencia.
Mi posición es Engineer en la compañía Andes. Mi experiencia es de 3 años.
My position is Engineer at Andes; I have 3 years of experience.
Egresada del programa de Sistemas de la Universidad Icesi; teléfono institucional +57-2-5551234.
Graduate of the program Computer Science at Icesi University; institution phone +57-2-5551234.
```

Multiple records retain the years/phone adjacent to each anchored record. Partial experience remains in `experience_mentions`; employers and programs are not inferred. Common email, location, GitHub and phone evidence is independent of profile.

The combined skill regex tries longer aliases first, so React.js does not also create a JavaScript claim through its JS suffix. Whitespace inside multiword aliases is flexible. Word boundaries prevent Pythonista, SQLAlchemy, GitHub and GitLab from counting as skill claims. Emails and HTTP URLs are masked.

Skills are tool claims such as `Python`, `Postgres` or `RESTful API`. Competences are explicit declarations such as `Tengo un nivel 4 en Version Control` or `Programming (level 3)`. These declarations are captured separately and masked before skill matching. Parenthetical technology levels remain legacy evidence but never become invented competence areas. No profile decision or alias normalization occurs in extraction.

Unsupported vocabulary and arbitrary layouts need additional documented patterns; this bounded model does not interpret negation.
