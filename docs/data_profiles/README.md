# Machine Learning and Data Architect

This folder documents Luis Eduardo Grijalba Franco's two assigned profiles. Start with [the profile contract](profile_contract.md), then [extraction](extraction.md) and the generated formal definitions for [Machine Learning](machine_learning.md) and [Data Architect](data_architect.md).

From the repository root:

```text
python -m pip install -r requirements.txt
python -m unittest discover -s tests/data_profiles -v
python -m src.data_pipeline examples/data_profiles/ml_engineer.txt --profile machine_learning
python -m src.data_pipeline examples/data_profiles/data_architect.txt --profile data_architect
python -m src.data_app examples/data_profiles/ml_and_architect.txt --output-dir output/demo_combined
python -m streamlit run src/data_web.py --server.address 127.0.0.1
python -m scripts.build_data_docs
python -m scripts.build_data_examples
```

The same engine runs both profiles. `examples/data_profiles/` contains five complete fictional résumés (ML and Data Architect in Spanish/English, plus both) and two incomplete cases. `output/data_profiles/` contains seven JSON reports and five validated DSL/Markdown exports. Five parsed candidate trees appear in `diagrams/*_tree.svg` and `.dot`. The build report checks syntax and business rules, not just DFA acceptance.

The console interface evaluates all available profile configurations by default or a single `--profile`. It prints accepted/rejected patterns and missing categories and saves `report.json`. A complete accepted candidate also produces `candidate.resume` and `candidate.md`, preserving every accepted classification. Missing source fields or declared levels block export without changing the DFA result. Use a new output folder on each run to avoid overwriting results. This interface currently exposes Luis's two profiles; it is not a claim that the team's other two profiles are implemented.

## Module design

| Module | Input | Output |
|---|---|---|
| `src/data_profiles.py` | Team qualification criteria | Vocabulary, aliases and ordered required categories |
| `src/stage1/extract_data.py` | Résumé text and profile key | Candidate fields, raw terms, declared levels |
| `src/stage2/normalize_data.py` | Raw terms and profile key | FST-normalized terms, unknown terms, canonical order |
| `src/stage3/classify_data.py` | Ordered canonical terms | DFA acceptance, missing categories, transition trace |
| `src/data_pipeline.py` | Text and profile key | Combined JSON report and optional DSL serialization |
| `src/data_app.py` | Text file, profile selection, output folder | Console summary, report, validated DSL and Markdown |
| `src/data_web.py` | Text or UTF-8 file and profile selection | Interactive stages, traces, report download and validated candidate downloads |
| `scripts/build_data_examples.py` | Source fixtures | JSON, validated DSL/Markdown, candidate trees and verification report |
| `scripts/build_data_docs.py` | Profile configurations and formal models | Formal definitions, full transition matrices, DOT and SVG diagrams |

## Verification scenarios

The Streamlit interface is optional: both interfaces call `analyze_text` and the same pipeline. A changed input cannot download stale outputs. Accepted-but-incomplete candidates show a blocked export, not invented data; rejected patterns still have downloadable diagnostic reports.

Tests check aliases, duplicates, unknown tokens, incorrect keyword substrings, every missing category, repeated alternatives, noncanonical DFA input, résumé order independence, Unicode names and repeated candidate records. Integration tests validate and render the ML export with the existing textX grammar and check that levels and identity are never fabricated.

Data Architect now passes stage 4; the previous Software Architect syntax label is preserved only for historical Follow-up 3 compatibility. See [readiness](readiness.md) for the requirement audit, [test scenarios](test_scenarios.md), [literature review](literature_review.md) and [defense practice](defense.md). The team still needs the other two classifiers, its final combined poster and presentation. Passing this suite does not claim that the whole integradora is finished.

## Technical references

- [Python regular expressions](https://docs.python.org/3/library/re.html): matching boundaries, alternatives, Unicode and case-insensitive flags inform the extraction design.
- [pyformlang FST](https://pyformlang.readthedocs.io/en/latest/modules/fst.html): `add_transition` and `translate` implement alias-to-canonical transformations as finite-state transducers.
- [pyformlang finite automata](https://pyformlang.readthedocs.io/en/latest/modules/finite_automaton.html): deterministic transitions and `accepts` provide the executable profile models.
- [textX metamodel](https://textx.github.io/textX/metamodel.html): the existing grammar produces structured objects consumed by the existing Markdown renderer.
- [Streamlit AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest): interactive tests exercise analysis, downloads, blocked/rejected cases and changed inputs.

These are implementation references, not a replacement for the team's broader literature review. The models deliberately separate raw matching, equivalence normalization and profile recognition.
