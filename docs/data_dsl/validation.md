# Current validation and outputs

Run `python -m src.candidate_validation <file.resume>` for an integrated candidate.
This parses the standalone representation, checks nonempty records, duplicates,
email and institutional phone constraints, then parses and validates with the
published contributor grammar. Experience years must be 1..59 inclusive; area
levels must be 1..5. Neither zero nor sixty years is valid for integration.

For a source resume, run `python -m src.data_app <file.txt-or-pdf> --output-dir <new-folder>`.
If at least one profile accepts and all mandatory fields/levels exist, the folder
contains report.json, candidate.resume and candidate.md. Otherwise the JSON
keeps the classification evidence and explains a rejected pattern or blocked
export. Existing result files are not overwritten.

For an existing DSL, validate with candidate_validation before running
`python -m src.data_dsl.markdown_generator <file.resume> --output <output-file.md>`.
The latter is a standalone helper and, by itself, does not impose the additional
integrated four-profile policy. It must not be used to claim an integrated
candidate is valid without that prior check.

The classifier output cannot manufacture missing identity, records, proficiency
levels or experience years. A classification result and a valid export are two
different outcomes. The old standalone validator permits 0..60 for historical
compatibility; only the integrated wrapper defines the current export contract.

Run `python run_local.py tests` to execute unittest classes and the published
function-style tests from all stages. The test count must come from the current
run, not from an old report.
