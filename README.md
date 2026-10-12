# ResumeLens - LeemStarTeam

ResumeLens extracts explicit evidence from technical resumes, normalizes aliases
with finite-state transducers, recognizes four qualification patterns with finite
automata, and validates a structured candidate with textX before Markdown export.
A candidate can satisfy none, one or several profiles: Full Stack Developer,
Machine Learning Engineer, Cybersecurity Specialist and Data Architect.

## Team and contributions

- Emmanuel Munoz (`emmanue1909`): Full Stack/Cybersecurity extraction, normalization
  and classifiers; published assembler, grammar, validator, PDF reader and tests.
- Luis Eduardo Grijalba Franco (`LuisEduardoGF`): ML/Data Architect models,
  shared data-profile workflow, compatibility adapters, CLI/web, exports and tests.

The integration preserves both Git histories and the contributor source at
revision `4a102a7`. Shared helpers and integration changes are described in
[the integration guide](docs/integration.md).

## Install and run

Python 3.12 was used for verification. In PowerShell, from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
python -m src.data_app examples/data_profiles/all_four.pdf --output-dir output/demo
python -m streamlit run src/data_web.py --server.address 127.0.0.1
python run_local.py tests
```

Select a new output directory for each console run. Its JSON report describes
accepted/rejected patterns, missing categories and evidence. A complete accepted
candidate also produces `candidate.resume` and `candidate.md`. The web and CLI
execute the same engine. Input supports UTF-8 text and PDFs with selectable text;
no OCR is implemented. See [input/output and validation](docs/data_dsl/validation.md).

## Validate an existing DSL and generate Markdown

Three current DSL examples are in `examples/current_dsl/`: ML, Cybersecurity and
one candidate satisfying all four profiles. Validate using the integrated rules:

```powershell
python -m src.candidate_validation examples/current_dsl/all_four.resume
if ($LASTEXITCODE -eq 0) {
    python -m src.data_dsl.markdown_generator examples/current_dsl/all_four.resume --output output/current_dsl/all_four.md
}
```

`candidate_validation` requires both the standalone model rules and Emmanuel's
four-profile grammar/validator. The integrated range is **1..59 years**, with
qualification levels **1..5**. Identity and proficiency are never invented.

The three older `examples/resume_*.resume` files are historical Follow-up DSL
examples. `resume_03` contains Software Architect, accepted only by the historical
standalone grammar in `src/data_dsl`; it is not a fifth integrated classifier.
The historical helpers are retained to reproduce earlier artifacts. Current
candidate exports should always use `candidate_validation` first.

## Repository map

| Path | Purpose |
|---|---|
| `src/data_profiles.py`, `src/stage1/extract_data.py`, `src/stage2/normalize_data.py`, `src/stage3/classify_data.py` | Shared configuration and four-profile data pipeline |
| `src/data_app.py`, `src/data_web.py`, `src/resume_input.py` | Common console/web engine and text/PDF inputs |
| `src/stage1` through `src/stage4` | Published contributor modules, retained without editing his source |
| `src/emmanuel_bridge.py`, `src/vendor/emmanuel_4a102a7/` | Integration bindings and hash-checked contributor source |
| `src/data_dsl/`, `src/candidate_validation.py` | Standalone DSL helpers and current integrated validation |
| `examples/data_profiles/`, `examples/current_dsl/` | Fictional source resumes and three current parsed examples |
| `output/data_profiles/` | Twelve diagnostic scenarios; eight complete DSL/Markdown exports |
| `docs/data_profiles/` | Regex, FST/DFA definitions, diagrams, scenarios, research and defense notes |
| `docs/data_dsl/` | Current entry guide, grammar explanation, decisions and validation commands |
| `docs/stage4/` | Contributor's earlier documentation, preserved; use the current guide for integration commands |
| `scripts/`, `tests/` | Reproducible document/example builders and both contributors' tests |

Start with [the current guide](docs/data_dsl/start_here.md), [the shared models](docs/data_profiles/shared_models.md),
[the profile contract](docs/data_profiles/profile_contract.md) and [verification scenarios](docs/data_profiles/test_scenarios.md).
The formal tables describe the actual executable models and are compared in tests.

## Limits and interpretation

Recognition verifies explicitly stated qualification patterns, not real competence,
truthfulness or hiring suitability. Regex anchors support bounded layouts and do
not interpret negation. Pattern acceptance is separate from exportability: a
candidate can match a profile but lack mandatory records or explicit area levels.
The AND/OR categories and year bounds are team policies, not universal professional
definitions. No real-world hiring accuracy has been measured.
