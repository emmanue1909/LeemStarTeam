import re


#def extract_skills_fullstack(text):
#    pattern = re.compile(r"\b(JavaScript|TypeScript|React|Angular|Vue|Node\.js|Django|Spring\sBoot|SQL|NoSQL|APIs\sREST|Git)\b", re.IGNORECASE)
#    return pattern.findall(text)

def extract_skill_javascript(text):
    pattern = re.compile(r"\b(JavaScript|Java\sScript|JS)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_typescript(text):
    pattern = re.compile(r"\b(TypeScript|Type\sScript|TS)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_react(text):
    pattern = re.compile(r"\b(React\.js|ReactJS|React)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_angular(text):
    pattern = re.compile(r"\b(AngularJS|Angular)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_vue(text):
    pattern = re.compile(r"\b(Vue\.js|VueJS|Vue)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_nodejs(text):
    pattern = re.compile(r"\b(Node\.js|NodeJS|Node)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_django(text):
    pattern = re.compile(r"\b(Django)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_springboot(text):
    pattern = re.compile(r"\b(Spring\sBoot|SpringBoot)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_sql(text):
    pattern = re.compile(r"\b(PostgreSQL|MySQL|Postgres|SQL)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_nosql(text):
    pattern = re.compile(r"\b(NoSQL|MongoDB|Mongo)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_apis_rest(text):
    pattern = re.compile(r"\b(RESTful\sAPI|APIs\sREST|API\sREST|REST\sAPI)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_git(text):
    pattern = re.compile(r"\b(Git)\b", re.IGNORECASE)
    return pattern.findall(text)


#def extract_qualifications_fullstack(text):
#    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Frontend\sDevelopment|Backend\sDevelopment|Database\sManagement|API\sIntegration|Version\sControl)\b", re.IGNORECASE)
#    return pattern.findall(text)

def extract_qualifications_frontend_fullstack(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Frontend\sDevelopment)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_qualifications_backend_fullstack(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Backend\sDevelopment)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_qualifications_database_fullstack(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Database\sManagement)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_qualifications_api_fullstack(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(API\sIntegration)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_qualifications_versioncontrol_fullstack(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Version\sControl)\b", re.IGNORECASE)
    return pattern.findall(text)

#def extract_qualifications_cybersecurity(text):
#    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Security\sTools|Security\sPractices|Cloud\sSecurity|Version\sControl)\b", re.IGNORECASE)
#    return pattern.findall(text)

def extract_qualifications_securitytools_cyber(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Security\sTools)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_qualifications_securitypractices_cyber(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Security\sPractices)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_qualifications_cloudsecurity_cyber(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Cloud\sSecurity)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_qualifications_versioncontrol_cyber(text):
    pattern = re.compile(r"tengo un nivel ([1-5]) en \b(Version\sControl)\b", re.IGNORECASE)
    return pattern.findall(text)

#def extract_skills_cybersecurity(text):
#    pattern = re.compile(r"\b(Nmap|Wireshark|Burp\sSuite|Metasploit|Penetration\sTesting|Vulnerability\sAssessment|OWASP|Incident\sResponse|AWS\sSecurity|Azure\sSecurity|Git|CEH|OSCP|Security\+)(?!\w)", re.IGNORECASE)
#    return pattern.findall(text)

def extract_skill_nmap(text):
    pattern = re.compile(r"\b(Network\sMapper|Nmap)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_wireshark(text):
    pattern = re.compile(r"\b(Wireshark)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_burpsuite(text):
    pattern = re.compile(r"\b(Burp\sSuite|BurpSuite|Burp)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_metasploit(text):
    pattern = re.compile(r"\b(Metasploit\sFramework|Metasploit)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_pentest(text):
    pattern = re.compile(r"\b(Penetration\sTesting|Pentesting|PenTest|Pentest)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_vulnassessment(text):
    pattern = re.compile(r"\b(Vulnerability\sAssessment)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_owasp(text):
    pattern = re.compile(r"\b(Open\sWeb\sApplication\sSecurity\sProject|OWASP)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_incidentresponse(text):
    pattern = re.compile(r"\b(Incident\sResponse)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_awssecurity(text):
    pattern = re.compile(r"\b(Amazon\sWeb\sServices\sSecurity|AWS\sSecurity)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_azuresecurity(text):
    pattern = re.compile(r"\b(Microsoft\sAzure\sSecurity|Azure\sSecurity)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_git_cyber(text):
    pattern = re.compile(r"\b(Git)\b", re.IGNORECASE)
    return pattern.findall(text)

#Certifications

def extract_skill_ceh(text):
    pattern = re.compile(r"\b(Certified\sEthical\sHacker|CEH)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_oscp(text):
    pattern = re.compile(r"\b(Offensive\sSecurity\sCertified\sProfessional|OSCP)\b", re.IGNORECASE)
    return pattern.findall(text)

def extract_skill_securityplus(text):
    pattern = re.compile(r"\b(CompTIA\sSecurity\+|Security\+)(?!\w)", re.IGNORECASE)
    return pattern.findall(text)