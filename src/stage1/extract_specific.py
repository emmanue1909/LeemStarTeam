import re


def extract_skills_fullstack(text):
    pattern = re.compile(r"\b(JavaScript|TypeScript|React|Angular|Vue|Node\.js|Django|Spring\sBoot|SQL|NoSQL|APIs\sREST|Git)\b", re.IGNORECASE)
    return pattern.findall(text)


def extract_qualifications_fullstack(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Frontend\sDevelopment|Backend\sDevelopment|Database\sManagement|API\sIntegration|Version\sControl)\b", re.IGNORECASE)
    return pattern.findall(text)


def extract_qualifications_cybersecurity(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Security\sTools|Security\sPractices|Cloud\sSecurity|Version\sControl)\b", re.IGNORECASE)
    return pattern.findall(text)


def extract_skills_cybersecurity(text):
    pattern = re.compile(r"\b(Nmap|Wireshark|Burp\sSuite|Metasploit|Penetration\sTesting|Vulnerability\sAssessment|OWASP|Incident\sResponse|AWS\sSecurity|Azure\sSecurity|Git|CEH|OSCP|Security\+)(?!\w)", re.IGNORECASE)
    return pattern.findall(text)