# Data profile contract

This contribution implements Machine Learning Engineer and Data Architect through extraction, normalization, classification and validated DSL/Markdown visualization. Both profiles use the same stage builders and shared textX grammar. Emmanuel's Full Stack and Cybersecurity definitions can be supplied through the same configuration format, with their own criteria and tests; those classifiers are not implemented here.

The source is the official ResumeLens assignment and Emmanuel's `ResumeLens_Perfiles_Division.docx`. The document lists qualifications but does not specify every AND/OR rule. Luis confirmed on 2026-10-08 that the following criteria are agreed with Emmanuel: **all categories are required; one alternative within each category is sufficient**. This is the team's explicit acceptance policy, not a rule or approval attributed to the instructor.

| Profile | Required categories in canonical order |
|---|---|
| Machine Learning Engineer | Python; Pandas or NumPy; Scikit-learn or TensorFlow or PyTorch; SQL or PostgreSQL or MySQL; Git |
| Data Architect | Data Modeling or Dimensional Modeling; Snowflake or BigQuery or Redshift; Spark or Airflow or Kafka; AWS or Azure or GCP; Python; SQL or PostgreSQL or MySQL; Git |

The Data Architect pattern requires Python and an SQL technology separately. This is a design choice rather than a rule explicitly dictated by the assignment. The SQL category preserves database tokens such as POSTGRESQL instead of incorrectly renaming them to SQL. This also accepts the assignment's ML automaton example containing PostgreSQL.

Data Architect requires explicit modeling evidence. The example in the division document lacked such a term; the new fictional example includes `Data Modeling`. Acceptance means matching a qualification pattern, not confirming proficiency or suitability for employment.

## Shared interfaces

1. `extract(text, profile)` returns candidate fields, raw qualification spellings and explicitly declared levels. It performs no canonical translation or profile decision.
2. `normalize(raw_terms, profile)` returns canonical tokens and unrecognized inputs using a pyformlang FST. Equivalent aliases are deduplicated.
3. `canonical_order(tokens, profile)` sorts by profile categories, making the résumé's original ordering irrelevant.
4. `classify(ordered_tokens, profile)` returns acceptance, missing categories and the actual DFA execution trace.
5. `run_pipeline(text, profile)` combines the stages. `to_dsl` exports accepted candidates with complete source fields and declared proficiency levels.

Profile configurations contain a display `label`, `variants` mapping canonical tokens to raw aliases, and ordered `categories` containing a name and alternative tokens. Categories must be disjoint and cover the vocabulary. The shared implementation does not contain separate hard-coded recognition algorithms for the two profiles.

## Boundaries

- Qualification extraction recognizes positive keyword occurrences; it does not interpret negation, sentiment or implied expertise. Email addresses and HTTP URLs are excluded from qualification matching.
- Candidate records use the bounded Spanish/English anchors documented in `extraction.md`. Partial experience mentions remain evidence, not fabricated employer records. Other résumé layouts need additional documented patterns.
- Years are extracted as written. DSL export uses 0..60, matching the existing validator; the team's current prose says 1..59 and needs reconciliation.
- No level is inferred from the presence of a skill. DSL export requires levels explicitly supplied as `Python (nivel 4)` or `Python (level 4)` and rejects inconsistent aliases or values outside 1..5.
- Incomplete qualification patterns are rejected and retained in the JSON report; they are not exported as accepted DSL profiles.
- The stage-4 grammar now accepts Data Architect. Software Architect remains a legacy syntax label only to preserve the previous Follow-up 3 examples; it is not a fifth classifier in the integradora. Both data profiles validate and generate Markdown, including a candidate accepted by both patterns.

All sample candidates, contacts, employers and declared levels are fictional test inputs. Luis's contribution covers these two data profiles and their tests and formal documents; this file does not claim implementation of Emmanuel's two profiles.
