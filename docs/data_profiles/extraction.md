# Extraction design

Implementation: `src/stage1/extract_data.py`. The `re` module detects candidate information and the textual variants listed in `src/data_profiles.py`.

| Field | Recognized source pattern | Output |
|---|---|---|
| Name | First nonblank line, 2 to 4 words consisting of Unicode letters, with internal apostrophes or hyphens | Original name or null |
| Location | `radicado en`, `radicada en`, `ubicación:` or `based in`, up to a period, semicolon or newline | Original location |
| Email | Local part, `@`, and a domain containing at least one dot | Original email |
| GitHub | `usuario de GitHub es` or `GitHub:` followed by a handle | Optional handle |
| Experience | `mi posición es <position> en la compañía <company>; tengo <integer> años de experiencia` or `my position is <position> at <company>; I have <integer> years of experience` | Repeated position, company and years records |
| Education | `egresado/egresada del programa de <program> de la <institution>; teléfono institucional <phone>` or `graduate of the program <program> at <institution>; institution phone <phone>` | Repeated education records |
| Partial experience | `<integer> years of experience ...` or `<integer> años de experiencia ...` | Original `experience_mentions`; not a complete employment record |
| Institution phone | `+<1..3 digits>-<1..4 digits>-<4..10 digits>` | Original phone |
| Qualifications | One bounded alternation of all profile aliases, sorted longest first; matches ignore case and allow repeated whitespace inside multiword aliases | Raw matched spellings in source order |
| Declared levels | `<term> (nivel <integer>)` or `<term> (level <integer>)` | Raw term and numeric declaration; no inferred value |

The executable constants in the module contain the exact regular expressions. The generated per-profile documents list the full qualification expression for each canonical term. Before extracting qualifications, email and HTTP URL substrings are masked to avoid treating a contact value as a qualification claim. Word boundaries prevent `SQLAlchemy`, `NoSQL`, `Pythonista` or `GitHub` from being mistaken for the shorter keywords SQL, Python or Git.

Missing candidate fields remain missing. Later export reports them rather than adding invented identity, employer or education information. Name, contact and experience extraction is independent of acceptance by the qualification automaton.

These are explicit Spanish/English templates, not a general CV parser. An official-style fragment may have enough qualifications to match a profile while lacking contact, employer, education or declared levels: it remains accepted by the DFA but cannot be exported as a complete candidate. Partial experience mentions are preserved without inventing a job.

Tests: `tests/data_profiles/test_extraction.py` covers spelling preservation, longest aliases, word boundaries, excluded contacts, case and whitespace, Unicode names, repeated records, English templates and incomplete fragments.
