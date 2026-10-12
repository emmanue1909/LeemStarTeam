# Literature and implementation review

This focused review supports the shared four-profile pipeline. It extends the earlier DSL work; it does not claim that research was completed before the first historical implementation. Consult the linked sources for the complete methods.

## Sources and design implications

1. Romero, J. (2021). *Pyformlang: An Educational Library for Formal Language Manipulation*. SIGCSE. [Author-maintained citation and implementation](https://github.com/Aunsiels/pyformlang), DOI [10.1145/3408877.3432464](https://doi.org/10.1145/3408877.3432464).

   The library provides executable formal-language models. We use actual transition objects and acceptance/translation methods so the formal definitions can be tested against implementation.

2. Dejanović, I., Vaderna, R., Milosavljević, G., and Vuković, Ž. (2017). *TextX: A Python tool for Domain-Specific Languages implementation*. Knowledge-Based Systems, 115, 1–4. [Authors' project description and citation](https://textx.github.io/textX/index.html), DOI [10.1016/j.knosys.2016.10.023](https://doi.org/10.1016/j.knosys.2016.10.023).

   A grammar produces a parser, metamodel and candidate object graph. We render that parsed model rather than formatting an unvalidated raw résumé. Business rules are checked separately from syntax.

3. Raza, M., and Gulwani, S. (2017). *Automated Data Extraction using Predictive Program Synthesis*. AAAI. [Microsoft Research publication abstract](https://www.microsoft.com/en-us/research/publication/automated-data-extraction-using-predictive-program-synthesis/).

   This work presents inference of extraction DSLs from examples. It is an alternative direction, not a technique implemented here: our smaller course model uses explicit regex anchors, avoiding claims of learned or layout-independent extraction.

4. [Python `re` documentation](https://docs.python.org/3/library/re.html), [pyformlang FST API](https://pyformlang.readthedocs.io/en/latest/modules/fst.html), [finite automaton API](https://pyformlang.readthedocs.io/en/latest/modules/finite_automaton.html), and [textX metamodel documentation](https://textx.github.io/textX/metamodel.html).

   These are implementation references, distinct from research papers. They inform boundary-aware matching, atomic-token alphabets, FST translation, DFA acceptance and model construction.

## Chosen approach and limitations

The processing stages have different responsibilities: regex finds evidence, FST translates aliases, sorting establishes an explicit profile order, DFA recognizes the category language, and textX plus business rules validates the exported candidate. The data profiles use C1+ C2+ … Ck+ after canonical sorting. The integrated Full Stack/Cybersecurity models use subset coverage and preserve the published acceptance policy. Neither is a universal definition of professional competence.

We preserve all satisfied profiles rather than imposing a single winner. Explicit lexical evidence cannot establish proficiency or truthfulness, and a negated term can still be matched. Missing identity, records or declared competence-area levels are reported instead of invented. This model is auditable but narrower than general résumé understanding.

textX's executable parser uses PEG machinery; the course EBNF describes the intended structured language. Do not confuse those descriptions with a proof of a minimal grammar or claim that this project implements general semantic understanding.

The same formal-language references support all four profile models; the final poster should connect them to each modeling decision. No hiring-performance comparison or real-world accuracy metric has been measured.
