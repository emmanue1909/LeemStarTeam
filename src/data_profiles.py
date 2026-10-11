"""Shared technology vocabulary and profile-specific acceptance patterns."""

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

PROFILES.update({
    'full_stack': {
        'label': 'Full Stack Developer',
        'variants': {
            **COMMON,
            'JAVASCRIPT': ['JavaScript', 'Java Script', 'JS'],
            'TYPESCRIPT': ['TypeScript', 'Type Script', 'TS'],
            'REACT': ['React.js', 'ReactJS', 'React'],
            'ANGULAR': ['Angular', 'AngularJS'],
            'VUE': ['Vue.js', 'VueJS', 'Vue'],
            'NODEJS': ['Node.js', 'NodeJS', 'Node JS', 'Node'],
            'DJANGO': ['Django'],
            'SPRING_BOOT': ['Spring Boot', 'SpringBoot'],
            'NOSQL': ['NoSQL'], 'MONGODB': ['MongoDB', 'Mongo DB', 'Mongo'],
            'REST_API': ['RESTful API', 'REST API', 'APIs REST', 'API REST', 'REST APIs'],
        },
        'categories': [
            ('Frontend development', ['JAVASCRIPT', 'TYPESCRIPT', 'REACT', 'ANGULAR', 'VUE']),
            ('Backend development', ['NODEJS', 'DJANGO', 'SPRING_BOOT']),
            ('Database management', ['SQL', 'POSTGRESQL', 'MYSQL', 'NOSQL', 'MONGODB']),
            ('API integration', ['REST_API']), ('Version control', ['GIT']),
        ],
    },
    'cybersecurity': {
        'label': 'Cybersecurity Specialist',
        'variants': {
            'GIT': ['Git'], 'NMAP': ['Nmap', 'Network Mapper'], 'WIRESHARK': ['Wireshark'],
            'BURP_SUITE': ['Burp Suite', 'BurpSuite', 'Burp'],
            'METASPLOIT': ['Metasploit', 'Metasploit Framework'],
            'PENETRATION_TESTING': ['Penetration Testing', 'Pentesting', 'Pentest'],
            'VULNERABILITY_ASSESSMENT': ['Vulnerability Assessment', 'Vuln Assessment'],
            'OWASP': ['OWASP', 'Open Web Application Security Project'],
            'INCIDENT_RESPONSE': ['Incident Response'],
            'AWS_SECURITY': ['AWS Security', 'Amazon Web Services Security'],
            'AZURE_SECURITY': ['Azure Security', 'Microsoft Azure Security'],
            'CEH': ['CEH', 'Certified Ethical Hacker'],
            'OSCP': ['OSCP', 'Offensive Security Certified Professional'],
            'SECURITY_PLUS': ['Security+', 'CompTIA Security+'],
        },
        'categories': [
            ('Security tools', ['NMAP', 'WIRESHARK', 'BURP_SUITE', 'METASPLOIT']),
            ('Security practices', ['PENETRATION_TESTING', 'VULNERABILITY_ASSESSMENT', 'OWASP', 'INCIDENT_RESPONSE']),
            ('Cloud security', ['AWS_SECURITY', 'AZURE_SECURITY']), ('Version control', ['GIT']),
        ],
        'optional': ['CEH', 'OSCP', 'SECURITY_PLUS'],
    },
})

# Competence declarations are separate from technology claims. No proficiency is inferred.
QUALIFICATION_VARIANTS = {
    'PROGRAMMING': ['Programming', 'Programación'],
    'DATA_PROCESSING': ['Data Processing', 'Procesamiento de datos'],
    'MACHINE_LEARNING': ['Machine Learning', 'Aprendizaje automático'],
    'DATA_MODELING': ['Data Modeling', 'Data Modelling', 'Modelado de datos'],
    'ANALYTICAL_STORAGE': ['Analytical Storage', 'Almacenamiento analítico'],
    'DATA_PIPELINES': ['Data Pipelines', 'Pipelines de datos'],
    'CLOUD_PLATFORMS': ['Cloud Platforms', 'Plataformas cloud'],
    'FRONTEND_DEVELOPMENT': ['Frontend Development'],
    'BACKEND_DEVELOPMENT': ['Backend Development'],
    'DATABASE_MANAGEMENT': ['Database Management', 'Gestión de bases de datos'],
    'API_INTEGRATION': ['API Integration'],
    'VERSION_CONTROL': ['Version Control', 'Control de versiones'],
    'SECURITY_TOOLS': ['Security Tools'], 'SECURITY_PRACTICES': ['Security Practices'],
    'CLOUD_SECURITY': ['Cloud Security'],
}

for canonical, aliases in QUALIFICATION_VARIANTS.items():
    if canonical not in aliases:
        aliases.append(canonical)

SKILL_VARIANTS = {}
for spec in PROFILES.values():
    for canonical, aliases in spec['variants'].items():
        SKILL_VARIANTS.setdefault(canonical, [])
        SKILL_VARIANTS[canonical] = list(dict.fromkeys(SKILL_VARIANTS[canonical] + aliases + [canonical]))


def vocabulary(profile):
    return [token for _, tokens in PROFILES[profile]["categories"] for token in tokens] + PROFILES[profile].get('optional', [])


def lexical_token(text):
    return " ".join(text.casefold().split())
