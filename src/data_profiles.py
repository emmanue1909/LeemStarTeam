"""Qualification vocabulary and acceptance patterns for Luis's two profiles."""

COMMON = {
    "PYTHON": ["Python"],
    "SQL": ["SQL", "Structured Query Language"],
    "POSTGRESQL": ["PostgreSQL", "Postgres"],
    "MYSQL": ["MySQL"],
    "GIT": ["Git"],
}

PROFILES = {
    "machine_learning": {
        "label": "Machine Learning Engineer",
        "variants": {
            **COMMON,
            "PANDAS": ["Pandas"],
            "NUMPY": ["NumPy", "Num Py"],
            "SCIKIT_LEARN": ["Scikit-learn", "scikit learn", "sklearn"],
            "TENSORFLOW": ["TensorFlow", "Tensor Flow"],
            "PYTORCH": ["PyTorch", "Py Torch"],
        },
        "categories": [
            ("Programming", ["PYTHON"]),
            ("Data processing", ["PANDAS", "NUMPY"]),
            ("Machine learning library", ["SCIKIT_LEARN", "TENSORFLOW", "PYTORCH"]),
            ("SQL technology", ["SQL", "POSTGRESQL", "MYSQL"]),
            ("Version control", ["GIT"]),
        ],
    },
    "data_architect": {
        "label": "Data Architect",
        "variants": {
            **COMMON,
            "DATA_MODELING": ["Data Modeling", "Data Modelling", "Modelado de datos"],
            "DIMENSIONAL_MODELING": ["Dimensional Modeling", "Dimensional Modelling", "Modelado dimensional"],
            "SNOWFLAKE": ["Snowflake"],
            "BIGQUERY": ["BigQuery", "Big Query", "Google BigQuery"],
            "REDSHIFT": ["Redshift", "Amazon Redshift"],
            "SPARK": ["Spark", "Apache Spark", "PySpark"],
            "AIRFLOW": ["Airflow", "Apache Airflow"],
            "KAFKA": ["Kafka", "Apache Kafka"],
            "AWS": ["AWS", "Amazon Web Services"],
            "AZURE": ["Azure", "Microsoft Azure"],
            "GCP": ["GCP", "Google Cloud", "Google Cloud Platform"],
        },
        "categories": [
            ("Data modeling", ["DATA_MODELING", "DIMENSIONAL_MODELING"]),
            ("Analytical storage", ["SNOWFLAKE", "BIGQUERY", "REDSHIFT"]),
            ("Data pipelines", ["SPARK", "AIRFLOW", "KAFKA"]),
            ("Cloud", ["AWS", "AZURE", "GCP"]),
            ("Programming", ["PYTHON"]),
            ("SQL technology", ["SQL", "POSTGRESQL", "MYSQL"]),
            ("Version control", ["GIT"]),
        ],
    },
}


def vocabulary(profile):
    return [token for _, tokens in PROFILES[profile]["categories"] for token in tokens]


def lexical_token(text):
    return " ".join(text.casefold().split())
