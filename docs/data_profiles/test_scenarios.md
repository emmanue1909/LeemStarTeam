# Integration test scenarios

| Scenario | Expected behavior | Evidence |
|---|---|---|
| Each of four complete profiles | Accepted, parsed, validated and rendered | Generated Full Stack/Cybersecurity/ML/Data Architect fixtures |
| A required category missing | Rejected, category identified, no accepted export | Per-category tests for all profiles and four incomplete fixtures |
| Zero, one, two, four matches | Preserve every independent result and accepted classification | Integration tests and combined candidates |
| Anchored/first-line Unicode name | Same candidate identity | Ana Pérez and Julián Restrepo cases |
| Both employment formats; repeated jobs | Same common records; separate integer years | Compatibility and repeated-record tests |
| JS/JavaScript duplicates, React.js overlap, flexible spaces | One canonical claim; no JS suffix false positive | Skill regression tests |
| Postgres/PostgreSQL/MySQL | Detailed shared token in all profiles; database evidence for classification | FST and adapter tests |
| Area level, technology level, contradictory aliases | Only explicit competence declarations exported; conflicts blocked | Area/skill separation and level tests |
| Years 0, 1, 59, 60, 61; levels outside 1..5 | Only years 1..59 allowed; invalid boundaries rejected | Pipeline/validator tests |
| Optional certifications and extra known skills | Preserve evidence, do not require certificates or reject complete patterns | Cybersecurity and extras tests |
| Emmanuel subset classifier, all representative subsets and permutations | Adapter has identical acceptance | Published-model compatibility comparison |
| Wrong/missing DSL structure, duplicates, blank values | Parsing/business validation fails before rendering | Historical DSL fixtures and current validation tests |
| UI selection for four profiles, changed text, missing declarations | Valid downloads or explicit status; no stale candidate output | Streamlit AppTest scenarios |
| Formal tables/generated outputs | Match executable objects and fresh pipeline output | Artifact regression tests, including both shared FST tables |
| All 58 published Emmanuel skill aliases | Preserve complete raw spelling and compatible classifier symbols | Frozen `922c0d2` vocabulary fixture and regression tests |
| Complete security-cloud names | AWS_SECURITY/AZURE_SECURITY evidence; no partial plain-cloud match | Full Cybersecurity export tests |
| Ordered data models, all category subsets | Same result for forward/reverse résumé order and duplicates | 32 ML and 128 Data Architect subsets |

Additional bridge tests verify exact source hashes, sequential state names, native tuple qualifications, real assembler calls, serialization, standalone validation and text-based PDF input.

Run the full suite with `.venv/Scripts/python.exe run_local.py tests`. Scenario counts refer to fixtures or assertions, not empirical hiring accuracy. All candidate data is fictional.
