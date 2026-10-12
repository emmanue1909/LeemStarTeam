# Technical defense of the integrated pipeline

Explain which component performs each operation: regex preserves a raw match; the FST translates an atomic alias; the DFA consumes canonical skill symbols; textX parses a structured résumé; the business validator checks values; Markdown comes from that validated object model.

## Model choices

ML and Data Architect use ordered category languages C1+ C2+ ... Ck+. The pipeline sorts and deduplicates before recognition, so their ordered automata do not depend on résumé order. A state qi remembers that the first i categories are covered; invalid order goes to q_dead.

Full Stack and Cybersecurity retain Emmanuel's coverage-subset language. Their states remember any subset of covered areas: 32 and 16 states respectively. Their adapter changes symbol spelling and preserves PostgreSQL/MySQL as database evidence without losing the detailed names in the DSL. An irrelevant known symbol keeps coverage unchanged.

The shared skill and competence FSTs each have two states. An entire extracted alias is one atomic input symbol, even when its spelling contains several characters or words. Canonical equivalence is implemented by the FST; whitespace squeezing is lexical preparation. Levels do not come from the FST or from technology membership.

## Practice modifications

1. Predict the missing category after removing REST API from the Full Stack fixture; then run the program.
2. Explain why adding CEH cannot repair missing cloud-security evidence.
3. Trace Postgres through extraction, shared FST, classifier adapter and DSL; identify where SQL grouping occurs.
4. Remove the area-level declaration from an accepted candidate and explain why pattern acceptance stays true but export is blocked.
5. Compare Data Modeling as a skill with `Tengo un nivel 4 en Data Modeling` as a competence declaration.
6. Add a new alias, regenerate formal documents/examples and run the artifact tests.
7. Explain why four accepted labels represent four independent results and do not rank a candidate.

Use the validated all-four output and current formal diagrams in the English presentation. Avoid presenting historical Software Architect syntax examples as evidence of a current classifier. Tests establish behavior under the configured policy; they do not establish truthfulness or hiring suitability.
