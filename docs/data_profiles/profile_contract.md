# Shared profile contract — version 3

The official assignment requires one general solution for four profiles and permits team-defined acceptance patterns and canonical sorting. This version preserves the existing ML/Data Architect criteria and uses Emmanuel's newly published Full Stack/Cybersecurity coverage criteria. The integration decisions below are implemented local policies; no new agreement or instructor approval is asserted.

The archived contract records Luis's confirmation on 2026-10-08. Emmanuel's messages on 2026-10-10 identify unresolved standardization. This version makes those interfaces explicit without altering the historical record.

## Acceptance table

AND across rows of categories; OR within each category:

| Profile | Required categories |
|---|---|
| Full Stack Developer | JavaScript/TypeScript/React/Angular/Vue; Node.js/Django/Spring Boot; SQL/PostgreSQL/MySQL/NoSQL/MongoDB; REST APIs; Git |
| Machine Learning Engineer | Python; Pandas/NumPy; Scikit-learn/TensorFlow/PyTorch; SQL/PostgreSQL/MySQL; Git |
| Cybersecurity Specialist | Nmap/Wireshark/Burp Suite/Metasploit; Pentest/Vulnerability Assessment/OWASP/Incident Response; AWS Security/Azure Security; Git |
| Data Architect | Data/Dimensional Modeling; Snowflake/BigQuery/Redshift; Spark/Airflow/Kafka; AWS/Azure/GCP; Python; SQL/PostgreSQL/MySQL; Git |

Full Stack follows Emmanuel's broad frontend group: JavaScript or a frontend framework is sufficient for that category. Cybersecurity certifications CEH/OSCP/Security+ are optional. The two data criteria are retained rather than silently weakened: Data Architect needs both Python and an SQL technology, and explicit modeling. The division document's incomplete fragment is not treated as a complete accepted candidate. ML follows the official accepted automaton example, without adding a new mandatory model-development category.

## Interfaces

`extract(text, profile)` returns identical candidate/evidence structures for every profile:

```text
name, location, email, github, phone: string or None
experiences: [{position: string, company: string, years: int}]
experience_mentions: [original strings]
educations: [{program: string, institution: string, phone: string}]
raw_skills: [original matched technology strings]
raw_qualifications: [{term: original area string, level: int}]
declared_levels: legacy parenthetical evidence, not used to infer area competence
```

`normalize_skills` uses the shared skill FST, deduplicates and returns canonical technologies plus unknown terms. `normalize_qualifications` uses a separate area FST and retains explicit integer levels. It reports conflicting levels and values outside 1..5. Qualification statements are masked from skill matching; declaring a level in Data Modeling is not automatically a claim of the DATA_MODELING skill.

`run_pipeline(text, profile, normalized_profile=None)` consumes the published team normalizer for Full Stack/Cybersecurity and supports supplied skill/qualification payloads. Tuple declarations `(level, area)` and string integer levels are adapted internally; supported additional explicit declarations are retained. It returns `contract_version=3`, profile label, extracted evidence, `skills`, `qualifications`, `qualification_errors`, `classification_input`, acceptance, missing categories and DFA trace. Every profile sees the same normalized evidence; its input projection contains its applicable technology vocabulary, sorted by configured category. Known extra technologies remain in the candidate output but do not satisfy unrelated categories.

Full Stack and Cybersecurity use the published 2f51e09 subset DFA with its sequential state names through an adapter: PostgreSQL/MySQL map to legacy SQL, MongoDB to legacy NOSQL, and underscores to the published spaced symbols. This mapping only affects classifier input. The DSL keeps the detailed shared tokens. Added known unrelated symbols loop. ML and Data Architect retain the ordered-category DFA, with ordering performed outside the automaton as allowed by the assignment.

## Export rules and boundaries

- Export requires at least one accepted profile and the mandatory fields/records of the existing grammar.
- Skills need no level. Qualifications represent explicitly declared areas, not duplicated technologies. Accepted patterns can still have export status BLOCKED when no area-level declaration is present.
- Years are extracted as original numeric evidence. Integrated export and `candidate_validation.py` enforce 1..59, following Emmanuel's published policy. His inherited 0..60 base validator is preserved unchanged; our stricter wrapper applies the current workflow limit. This is a team implementation policy, not a course requirement.
- At least one explicitly declared competence is required by the inherited `qualifications+=Qualification` grammar. No requirement to declare every category or to infer a level is added.
- `candidate_documents` merges every accepted classification for the same candidate, deduplicates shared evidence, then validates syntax and business rules before rendering.
- Names use Unicode 2–4-word anchored names or first-line names, with anchor priority. Records require documented sentence anchors and local association of years/phone; arbitrary prose and dotted company names need further patterns.
- Positive keyword matching does not understand negation, truthfulness or suitability. Unknown prose is not automatically normalized.

The legacy direct function `extract_qualifications(text, profile)` still returns profile technology spellings for earlier callers. Current integration callers use `extract(...)["raw_skills"]`; the legacy function does not define the version-3 qualification schema.

The unchanged published assembler receives Spanish record keys and `(integer level, canonical area)` qualification tuples from `emmanuel_bridge.py`. Both the active and published grammars validate generated candidates. The exact-source snapshot and adaptation details appear in [the final integration report](../integration_final_2026-10-11.md).
