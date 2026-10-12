# ResumeLens: ten-minute technical presentation

Use the English poster as the visual support. These time windows total ten minutes and include brief pauses to show the actual program; rehearse and adjust speaking speed. Speaker assignments should follow the team's real contributions.

## 0:00–1:00 — Problem and scope

Our project is ResumeLens. Its purpose is to recognize explicitly stated technical qualification patterns in resumes and produce a validated candidate representation. The problem is that equivalent technologies can appear under different spellings, and the same qualifications can appear in different orders.

We support Full Stack Developer, Machine Learning Engineer, Cybersecurity Specialist and Data Architect. A candidate may satisfy none, one or several patterns. We preserve every accepted classification. We do not rank people, verify their claims or make a hiring decision.

The poster organizes the solution into four stages: extraction, normalization, recognition and structured validation. Each stage has a different formal model and a different responsibility.

## 1:00–2:15 — Regex extraction

Stage one uses Python's regular-expression module. Technology aliases are ordered from longest to shortest so a complete name such as React.js is captured before a shorter suffix. The extractor preserves the spelling that occurred in the source text; it does not decide canonical equivalence.

Personal records use explicit sentence anchors. We support the team's name and employment phrases and an earlier first-line name format. Repeated jobs keep their own adjacent years. Education records associate their institutional phone locally rather than borrowing an unrelated phone from elsewhere in the resume.

We separate technology claims from competence-area declarations. For example, a declared level in Version Control is a qualification with an explicit integer level. It is not a proficiency value invented for every technology. These patterns have a bounded input language, and they do not understand negation.

## 2:15–3:30 — FST normalization

Stage two uses actual pyformlang finite-state transducers. We define the seven components: states, input alphabet, output alphabet, transition function, output function, initial state and final states.

In our abstraction, an entire extracted alias is one input symbol. It is not necessary to process every character separately. A two-state transducer consumes that alias and emits its canonical token. An unsupported input has no accepting translation.

The shared vocabulary preserves named database technologies. Postgres becomes POSTGRESQL, while MySQL remains MYSQL. Technologies and competence areas use separate namespaces. The published team normalizer supplies qualifications as level-and-area tuples; our bridge consumes that shape and keeps conflicting or invalid levels visible as validation errors.

## 3:30–5:10 — Automata and acceptance

Stage three uses actual deterministic finite automata. Each machine has a state set, input alphabet, transition function, initial state and accepting states. Each state-symbol pair has one destination and there are no epsilon transitions.

The ML and Data Architect models read category evidence in a canonical order, which the assignment explicitly permits. An ML state records how many initial categories have been covered. The ML machine has seven states, including its rejecting sink; Data Architect has nine. Alternatives within a category are an OR requirement, while the categories themselves are an AND requirement.

The Full Stack and Cybersecurity machines preserve Emmanuel's published coverage construction. Their states represent subsets of covered categories, so five categories require thirty-two states and four require sixteen. These machines accumulate coverage regardless of source order. Our adapter retains his sequential state names and maps detailed database tokens to his grouped classifier symbols.

Show the ML example on the poster: Python, Pandas, TensorFlow, Postgres and Git. Normalization gives PYTHON, PANDAS, TENSORFLOW, POSTGRESQL and GIT. The actual state trace reaches q5 and the pattern is accepted. Removing the machine-learning-library token leaves a required category missing.

## 5:10–6:25 — Grammar and validation

Stage four represents the result in a structured language. The textX grammar creates a candidate model with personal information, contact, repeated experience and education records, skills, declared qualifications and classifications.

Our bridge converts records into the unchanged team assembler's field names and qualification tuples. We then parse and validate its DSL output before generating Markdown. Syntax and business rules are separate checks: a parseable document can still contain conflicting levels or invalid experience years.

The integrated workflow follows the team's one-to-fifty-nine-year experience policy. Emmanuel's current validator also enforces those bounds. Our wrapper checks the candidate using both representations and keeps additional checks for missing fields, duplicates and conflicting levels. An accepted skill pattern can still have a blocked export. We report missing data instead of inventing it.

## 6:25–7:40 — Connected execution

Demonstrate the fictional four-profile input. Run:

```powershell
.\.venv\Scripts\python.exe -m src.data_app examples/data_profiles/all_four.pdf --output-dir output/presentation_demo
```

Use a new output directory, since previous results are protected. Show the four accepted patterns and the validated candidate output. In the web interface, show the extraction, normalization and DFA-trace sections and the DSL/Markdown downloads. Change the input and explain why stale results are hidden until analysis runs again.

PDF input uses the retained team reader. It requires selectable text. A scanned image PDF does not silently receive invented content; the program reports that there is no extractable text.

## 7:40–9:00 — Tests and results

The checked local version passed two hundred and forty automated tests: ninety-eight unittest cases and one hundred and forty-two function cases. The evidence includes twelve fictional scenarios: eight complete candidates produce validated exports and four incomplete patterns are rejected.

We test all fifty-eight published alias entries, including complete raw spellings. Other scenarios check missing categories, duplicates, reversed input order, optional certificates, unrelated skills, conflicting levels, boundary years, malformed DSL, PDF input and the Streamlit interface.

We also compare formal transition tables directly against executable machine objects. Source hashes verify that the contributor modules retained in the snapshot have not been edited. Specific integration tests confirm that the actual published normalizer and assembler are called and that the new state names remain unchanged.

These results establish behavior on the documented language and tested fixtures. They are not evidence of hiring accuracy on real people or unrestricted natural-language resumes.

## 9:00–10:00 — Limits and engineering conclusions

Our strongest property is traceability: a reviewer can follow the original evidence, the canonical tokens, the executed state transitions and the validated candidate model. The different model choices are compatible because their interfaces and preprocessing steps are explicit.

The main limitations are bounded layouts, keyword matching without negation understanding, explicitly required candidate fields and PDF text extraction without OCR. Future work could broaden extraction patterns, add OCR as a distinct preprocessing step and expand scenario coverage while preserving the model contracts.

The literature review connects the implementation to pyformlang and textX. The educational value is being able to explain what each symbol and state means, why the selected machine recognizes the intended language, and how a changed requirement changes its transitions and tests.
