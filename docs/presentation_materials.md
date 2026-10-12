# Research poster and ten-minute demonstration

The English poster is `output/pdf/ResumeLens_Poster_English.pdf`, landscape A2.
It contains the research question, the four-stage flow, an actual shared-FST
translation, an accepted/rejected ML trace, profile-state counts, fixture results,
conclusion, limitations and references. The body uses 18-21 pt; display labels
and headings are larger. Check physical readability at the intended print size.

The figures are vector drawings. The generator checks eight valid candidate
exports and four rejected incomplete patterns using the current executable
engine. The reported 240 cases correspond to the verified combined test runner.
This measures configured-language behavior, not real-world hiring accuracy.

Reproduce only after a fresh successful test run:

```powershell
python run_local.py tests
python -m scripts.build_delivery_materials --passed-tests 240
```

The generator's count argument must match actual verification; it is not a test
command. If the test suite changes, revise the poster case breakdown as well.

Use [the English script](presentation_english.md) for the ten-minute technical
presentation. Its time windows include the console/web demonstration. Rehearse
with both team members, follow their real contributions and be ready to explain
the symbol alphabets, FST outputs, DFA state meanings, canonical ordering,
grammar/model distinction and export constraints.

The class poster guides were consulted during review. This layout uses three
columns, a research question and more visual evidence than the earlier draft.
The references are Romero's pyformlang article and Dejanovic et al.'s textX paper.
Registration, course submission and individual rehearsal are external steps;
publishing these materials does not certify they occurred.
