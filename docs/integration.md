# Four-profile integration

This version combines the published histories of root-data and root-emmanuel.
Emmanuel's source and tests are retained at revision 4a102a7. His fixes to
JavaScript suffix matching and experience-year validation are included.

The integrated flow is extraction, FST normalization, canonical ordering where
required, profile automata, DSL validation and Markdown export. Console and web
use the same data_app/data_pipeline engine. Full Stack and Cybersecurity execute
the contributor normalizer and classifiers through emmanuel_bridge; the assembler,
PDF reader and validator are loaded from unchanged, hash-checked source files.

Our standalone DSL helpers moved from src/stage4 to src/data_dsl so integration
does not replace the contributor's source files. src/validator.py is a compatibility
import for the earlier standalone DSL test entry point. Current candidate export
also validates against the contributor's four-profile grammar, so the historical
Software Architect example does not become a fifth integrated classifier.

The src/vendor/emmanuel_4a102a7/SOURCE.json manifest records the exact source
revision and hashes. Tests compare the retained files against the manifest and
exercise the integrated contracts, accepted/rejected profiles and PDF inputs.

Final documentation cleanup and presentation materials are separate work blocks.
