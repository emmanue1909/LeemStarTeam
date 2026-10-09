# Data Architect formal models

## Stage 1 qualification expressions

All expressions use `re.IGNORECASE`. The extractor returns the original matched text.

| Term | Recognized aliases |
|---|---|
| DATA_MODELING | Data Modeling, Data Modelling, Modelado de datos |
| DIMENSIONAL_MODELING | Dimensional Modeling, Dimensional Modelling, Modelado dimensional |
| SNOWFLAKE | Snowflake |
| BIGQUERY | BigQuery, Big Query, Google BigQuery |
| REDSHIFT | Redshift, Amazon Redshift |
| SPARK | Spark, Apache Spark, PySpark |
| AIRFLOW | Airflow, Apache Airflow |
| KAFKA | Kafka, Apache Kafka |
| AWS | AWS, Amazon Web Services |
| AZURE | Azure, Microsoft Azure |
| GCP | GCP, Google Cloud, Google Cloud Platform |
| PYTHON | Python |
| SQL | SQL, Structured Query Language |
| POSTGRESQL | PostgreSQL, Postgres |
| MYSQL | MySQL |
| GIT | Git |

Exact expressions:

```text
DATA_MODELING: (?<!\w)(?:Modelado\s+de\s+datos|Data\s+Modelling|Data\s+Modeling)(?!\w)
DIMENSIONAL_MODELING: (?<!\w)(?:Dimensional\s+Modelling|Dimensional\s+Modeling|Modelado\s+dimensional)(?!\w)
SNOWFLAKE: (?<!\w)(?:Snowflake)(?!\w)
BIGQUERY: (?<!\w)(?:Google\s+BigQuery|Big\s+Query|BigQuery)(?!\w)
REDSHIFT: (?<!\w)(?:Amazon\s+Redshift|Redshift)(?!\w)
SPARK: (?<!\w)(?:Apache\s+Spark|PySpark|Spark)(?!\w)
AIRFLOW: (?<!\w)(?:Apache\s+Airflow|Airflow)(?!\w)
KAFKA: (?<!\w)(?:Apache\s+Kafka|Kafka)(?!\w)
AWS: (?<!\w)(?:Amazon\s+Web\s+Services|AWS)(?!\w)
AZURE: (?<!\w)(?:Microsoft\s+Azure|Azure)(?!\w)
GCP: (?<!\w)(?:Google\s+Cloud\s+Platform|Google\s+Cloud|GCP)(?!\w)
PYTHON: (?<!\w)(?:Python)(?!\w)
SQL: (?<!\w)(?:Structured\s+Query\s+Language|SQL)(?!\w)
POSTGRESQL: (?<!\w)(?:PostgreSQL|Postgres)(?!\w)
MYSQL: (?<!\w)(?:MySQL)(?!\w)
GIT: (?<!\w)(?:Git)(?!\w)
```

## Stage 2 finite state transducer

M = (Q, Sigma, Gamma, delta, omega, q0, F).

- Q = {q0, q1}; q0 is initial and F = {q1}.
- Sigma is the finite set of input tokens in the table below; each complete alias is one atomic symbol.
- Gamma = {DATA_MODELING, DIMENSIONAL_MODELING, SNOWFLAKE, BIGQUERY, REDSHIFT, SPARK, AIRFLOW, KAFKA, AWS, AZURE, GCP, PYTHON, SQL, POSTGRESQL, MYSQL, GIT}.
- For each table row (x, y): delta(q0, x) = q1 and omega(q0, x) = [y]. All other transitions are absent.
- The FST processes one extracted term at a time; it is reset between terms. An unknown term has no translation.
- Before translation, `casefold` and whitespace squeezing only unify the lexical representation. Alias equivalence is performed by the FST.

| Input token x | Output token y | delta | omega |
|---|---|---|---|
| `data modeling` | `DATA_MODELING` | q0 to q1 | [DATA_MODELING] |
| `data modelling` | `DATA_MODELING` | q0 to q1 | [DATA_MODELING] |
| `modelado de datos` | `DATA_MODELING` | q0 to q1 | [DATA_MODELING] |
| `dimensional modeling` | `DIMENSIONAL_MODELING` | q0 to q1 | [DIMENSIONAL_MODELING] |
| `dimensional modelling` | `DIMENSIONAL_MODELING` | q0 to q1 | [DIMENSIONAL_MODELING] |
| `modelado dimensional` | `DIMENSIONAL_MODELING` | q0 to q1 | [DIMENSIONAL_MODELING] |
| `snowflake` | `SNOWFLAKE` | q0 to q1 | [SNOWFLAKE] |
| `big query` | `BIGQUERY` | q0 to q1 | [BIGQUERY] |
| `bigquery` | `BIGQUERY` | q0 to q1 | [BIGQUERY] |
| `google bigquery` | `BIGQUERY` | q0 to q1 | [BIGQUERY] |
| `amazon redshift` | `REDSHIFT` | q0 to q1 | [REDSHIFT] |
| `redshift` | `REDSHIFT` | q0 to q1 | [REDSHIFT] |
| `apache spark` | `SPARK` | q0 to q1 | [SPARK] |
| `pyspark` | `SPARK` | q0 to q1 | [SPARK] |
| `spark` | `SPARK` | q0 to q1 | [SPARK] |
| `airflow` | `AIRFLOW` | q0 to q1 | [AIRFLOW] |
| `apache airflow` | `AIRFLOW` | q0 to q1 | [AIRFLOW] |
| `apache kafka` | `KAFKA` | q0 to q1 | [KAFKA] |
| `kafka` | `KAFKA` | q0 to q1 | [KAFKA] |
| `amazon web services` | `AWS` | q0 to q1 | [AWS] |
| `aws` | `AWS` | q0 to q1 | [AWS] |
| `azure` | `AZURE` | q0 to q1 | [AZURE] |
| `microsoft azure` | `AZURE` | q0 to q1 | [AZURE] |
| `gcp` | `GCP` | q0 to q1 | [GCP] |
| `google cloud` | `GCP` | q0 to q1 | [GCP] |
| `google cloud platform` | `GCP` | q0 to q1 | [GCP] |
| `python` | `PYTHON` | q0 to q1 | [PYTHON] |
| `sql` | `SQL` | q0 to q1 | [SQL] |
| `structured query language` | `SQL` | q0 to q1 | [SQL] |
| `postgres` | `POSTGRESQL` | q0 to q1 | [POSTGRESQL] |
| `postgresql` | `POSTGRESQL` | q0 to q1 | [POSTGRESQL] |
| `mysql` | `MYSQL` | q0 to q1 | [MYSQL] |
| `git` | `GIT` | q0 to q1 | [GIT] |

![FST diagram](diagrams/data_architect_fst.svg)

[Complete FST transition graph](diagrams/data_architect_fst.dot)

## Stage 3 deterministic finite automaton

M = (Q, Sigma, delta, q0, F).

- Q = {q0, q1, q2, q3, q4, q5, q6, q7, q_dead}.
- Sigma = {DATA_MODELING, DIMENSIONAL_MODELING, SNOWFLAKE, BIGQUERY, REDSHIFT, SPARK, AIRFLOW, KAFKA, AWS, AZURE, GCP, PYTHON, SQL, POSTGRESQL, MYSQL, GIT}.
- Initial state: q0. F = {q7}.
- delta is defined for every state and every symbol by the matrix below; q_dead is a nonaccepting sink.
- qi records that the first i categories have been satisfied. Repeated alternatives in the current category keep the same state.
- A skipped, decreasing or unknown category is rejected. The pipeline sorts and deduplicates first, so the résumé's original order does not affect the result.
- There is exactly one destination per state/symbol pair and no epsilon transition: this is a DFA.

The language is L = C1+ C2+ ... Ck+. Within each Ci, alternatives are OR; across categories, requirements are AND.

| Category | Required evidence |
|---|---|
| C1: Data modeling | DATA_MODELING or DIMENSIONAL_MODELING |
| C2: Analytical storage | SNOWFLAKE or BIGQUERY or REDSHIFT |
| C3: Data pipelines | SPARK or AIRFLOW or KAFKA |
| C4: Cloud | AWS or AZURE or GCP |
| C5: Programming | PYTHON |
| C6: SQL technology | SQL or POSTGRESQL or MYSQL |
| C7: Version control | GIT |

![DFA diagram](diagrams/data_architect_dfa.svg)

[All DFA edges in DOT format](diagrams/data_architect_dfa.dot)

## Full transition matrix

An arrow marks the initial state; * marks the accepting state.

| State | DATA_MODELING | DIMENSIONAL_MODELING | SNOWFLAKE | BIGQUERY | REDSHIFT | SPARK | AIRFLOW | KAFKA | AWS | AZURE | GCP | PYTHON | SQL | POSTGRESQL | MYSQL | GIT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| -> q0 | q1 | q1 | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead |
| q1 | q1 | q1 | q2 | q2 | q2 | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead |
| q2 | q_dead | q_dead | q2 | q2 | q2 | q3 | q3 | q3 | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead |
| q3 | q_dead | q_dead | q_dead | q_dead | q_dead | q3 | q3 | q3 | q4 | q4 | q4 | q_dead | q_dead | q_dead | q_dead | q_dead |
| q4 | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q4 | q4 | q4 | q5 | q_dead | q_dead | q_dead | q_dead |
| q5 | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q5 | q6 | q6 | q6 | q_dead |
| q6 | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q6 | q6 | q6 | q7 |
| * q7 | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q7 |
| q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead | q_dead |

## Limitations

The model recognizes explicitly named qualifications under the proposed category policy. It does not rank candidates, infer proficiency, handle negated claims or verify experience. Unrecognized résumé terms do not satisfy a required category.
