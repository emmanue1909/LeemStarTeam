# Four-profile models and shared pipeline

Luis's assigned profiles are [Machine Learning](machine_learning.md) and
[Data Architect](data_architect.md). The combined application also evaluates
[Full Stack](full_stack.md) and [Cybersecurity](cybersecurity.md) using the published
contributor models. See [the contract](profile_contract.md), [raw extraction](extraction.md),
[shared FSTs](shared_models.md) and [integration](../integration.md).

Each model document contains its alphabet, states, initial/final states,
transition function, diagram and acceptance policy. All FSTs include the complete
7-tuple; the API stores a single output symbol y as [y]. Whole aliases are atomic
input symbols. This abstraction is supported by Week4/Transducers.ipynb and the
course Streamlit Guide examples. Each alias is translated independently from q0.

Twelve fictional source scenarios produce twelve reports. Eight complete
candidates produce valid DSL/Markdown exports and tree diagrams; four incomplete
patterns reject. Tests compare tables, transitions, traces and regenerated outputs.
Run `python run_local.py tests` for the combined unittest/function-style suite.

The input supports UTF-8 text and text-based PDFs. Console and Streamlit share
analyze_text and the same pipeline. Missing mandatory fields or area levels block
export without changing an accepted pattern. Source identity and levels are never
invented. See [current validation](../data_dsl/validation.md).

Read [the literature review](literature_review.md), [test scenarios](test_scenarios.md)
and [defense notes](defense.md). These explain scope and limitations; successful
tests do not certify real-world hiring accuracy or replace an individual rehearsal.
