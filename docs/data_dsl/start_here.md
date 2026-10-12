# Current integrated DSL guide

The combined engine has four classifiers, not two: Full Stack, ML, Cybersecurity
and Data Architect. `src/data_app.py` and `src/data_web.py` call the same pipeline.
Follow raw extraction -> FST normalization -> DFA recognition -> assembler ->
textX and business validation -> Markdown. See [integration](../integration.md).

Start with `examples/current_dsl/all_four.resume` and validate it with
`python -m src.candidate_validation examples/current_dsl/all_four.resume`.
The accepted classification labels are preserved together in one candidate.

The current constraints are described in [validation](validation.md) and
[decisions](decisions.md). Original documents under `docs/stage4` are preserved
for contributor history; their old paths, two-profile descriptions and range
0..60 must not be read as the current integration contract.

The earlier standalone examples remain reproducible with `src/data_dsl`. Their
Software Architect example is historical and fails the integrated four-profile
grammar. Three current examples are provided separately and are validated with
both sets of rules. See [grammar and model](grammar.md).
