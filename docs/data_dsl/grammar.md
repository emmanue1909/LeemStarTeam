# Grammar, metamodel and candidate

The entry symbol is Resume. The intended structured language can be described
as G = (V, Sigma, Resume, P): V consists of the named rules in the .tx grammar;
Sigma contains its keywords, punctuation and lexical values; P is that rule set.
The integrated output must also belong to the contributor's four-profile grammar
in `src/stage4/grammar/resume.tx`. The standalone rules are in `src/data_dsl/grammar/resume.tx`.

Keywords include name, location, email, github, position, company, years,
institution, phone, program, skill, qualification, level and classification.
STRING holds quoted values; INT holds integers.
Experience, education, skill, qualification and classification records repeat.
textX assignments create attributes and lists in the candidate object graph.

For example, the skills part of Resume repeats Skill one or more times, and a
record derives `Skill -> skill STRING`, yielding `skill "PYTHON"`.
The semicolons in the .tx file terminate grammar rules; they are not serialized
after candidate records. Full examples include all mandatory records in order.
See the existing [terminal/nonterminal description](../stage4/Grammar.md) and
[metamodel](../stage4/Metamodel.md), read with the current integration constraints.

Classroom textX material follows grammar -> metamodel -> model -> interpretation.
metamodel_from_file creates the parser/classes; model_from_str/model_from_file
construct candidate instances. The validated object graph is then rendered as
Markdown and as a tree diagram. Business validation adds constraints beyond syntax.
