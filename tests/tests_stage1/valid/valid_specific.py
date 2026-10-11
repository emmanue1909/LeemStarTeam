import sys
from pathlib import Path
 
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
 
from src.stage1.extract_specific import (
    extract_skill_javascript, extract_skill_typescript, extract_skill_react,
    extract_skill_angular, extract_skill_vue, extract_skill_nodejs,
    extract_skill_django, extract_skill_springboot, extract_skill_sql,
    extract_skill_nosql, extract_skill_apis_rest, extract_skill_git,
    extract_qualifications_frontend_fullstack, extract_qualifications_backend_fullstack,
    extract_qualifications_database_fullstack, extract_qualifications_api_fullstack,
    extract_qualifications_versioncontrol_fullstack,
    extract_qualifications_securitytools_cyber, extract_qualifications_securitypractices_cyber,
    extract_qualifications_cloudsecurity_cyber, extract_qualifications_versioncontrol_cyber,
    extract_skill_nmap, extract_skill_wireshark, extract_skill_burpsuite,
    extract_skill_metasploit, extract_skill_pentest, extract_skill_vulnassessment,
    extract_skill_owasp, extract_skill_incidentresponse, extract_skill_awssecurity,
    extract_skill_azuresecurity, extract_skill_git_cyber,
    extract_skill_ceh, extract_skill_oscp, extract_skill_securityplus,
)
 
 
# ---------- Skills Full Stack ----------
 
def test_javascript_forma_completa():
    assert extract_skill_javascript("Tengo experiencia en JavaScript.") == ["JavaScript"]
 
 
def test_javascript_sigla_standalone():
    assert extract_skill_javascript("Trabajo con JS en el backend.") == ["JS"]
 
 
def test_typescript_forma_completa():
    assert extract_skill_typescript("Uso TypeScript en el proyecto.") == ["TypeScript"]
 
 
def test_typescript_forma_separada():
    assert extract_skill_typescript("Uso Type Script para tipado.") == ["Type Script"]
 
 
def test_react_con_punto():
    assert extract_skill_react("Trabajo con React.js en el frontend.") == ["React.js"]
 
 
def test_react_variante_reactjs():
    assert extract_skill_react("Tambien uso ReactJS.") == ["ReactJS"]
 
 
def test_angular_simple():
    assert extract_skill_angular("Uso Angular para SPA.") == ["Angular"]
 
 
def test_vue_con_punto():
    assert extract_skill_vue("Desarrollo con Vue.js.") == ["Vue.js"]
 
 
def test_nodejs_con_punto():
    assert extract_skill_nodejs("El backend esta en Node.js.") == ["Node.js"]
 
 
def test_django_simple():
    assert extract_skill_django("Uso Django para el backend.") == ["Django"]
 
 
def test_springboot_con_espacio():
    assert extract_skill_springboot("Trabajo con Spring Boot en Java.") == ["Spring Boot"]
 
 
def test_springboot_junto():
    assert extract_skill_springboot("Uso SpringBoot en microservicios.") == ["SpringBoot"]
 
 
def test_sql_variante_postgresql():
    assert extract_skill_sql("La base de datos es PostgreSQL.") == ["PostgreSQL"]
 
 
def test_nosql_variante_mongodb():
    assert extract_skill_nosql("Uso MongoDB como base de datos.") == ["MongoDB"]
 
 
def test_apis_rest_orden_rest_api():
    assert extract_skill_apis_rest("Diseno REST API para el backend.") == ["REST API"]
 
 
def test_apis_rest_orden_api_rest():
    assert extract_skill_apis_rest("Diseno API REST para el backend.") == ["API REST"]
 
 
def test_git_simple():
    assert extract_skill_git("Uso Git para control de versiones.") == ["Git"]
 
 
# ---------- Qualifications Full Stack ----------
 
def test_qualification_frontend_valido():
    assert extract_qualifications_frontend_fullstack(
        "Tengo un nivel 4 en Frontend Development."
    ) == [("4", "Frontend Development")]
 
 
def test_qualification_backend_valido():
    assert extract_qualifications_backend_fullstack(
        "Tengo un nivel 3 en Backend Development."
    ) == [("3", "Backend Development")]
 
 
def test_qualification_database_valido():
    assert extract_qualifications_database_fullstack(
        "Tengo un nivel 5 en Database Management."
    ) == [("5", "Database Management")]
 
 
def test_qualification_api_valido():
    assert extract_qualifications_api_fullstack(
        "Tengo un nivel 4 en API Integration."
    ) == [("4", "API Integration")]
 
 
def test_qualification_versioncontrol_fullstack_valido():
    assert extract_qualifications_versioncontrol_fullstack(
        "Tengo un nivel 5 en Version Control."
    ) == [("5", "Version Control")]
 
 
# ---------- Qualifications Cybersecurity ----------
 
def test_qualification_securitytools_valido():
    assert extract_qualifications_securitytools_cyber(
        "Tengo un nivel 4 en Security Tools."
    ) == [("4", "Security Tools")]
 
 
def test_qualification_securitypractices_valido():
    assert extract_qualifications_securitypractices_cyber(
        "Tengo un nivel 3 en Security Practices."
    ) == [("3", "Security Practices")]
 
 
def test_qualification_cloudsecurity_valido():
    assert extract_qualifications_cloudsecurity_cyber(
        "Tengo un nivel 4 en Cloud Security."
    ) == [("4", "Cloud Security")]
 
 
def test_qualification_versioncontrol_cyber_valido():
    assert extract_qualifications_versioncontrol_cyber(
        "Tengo un nivel 5 en Version Control."
    ) == [("5", "Version Control")]
 
 
# ---------- Skills Cybersecurity ----------
 
def test_nmap_simple():
    assert extract_skill_nmap("Uso Nmap para escaneo de redes.") == ["Nmap"]
 
 
def test_wireshark_simple():
    assert extract_skill_wireshark("Analizo trafico con Wireshark.") == ["Wireshark"]
 
 
def test_burpsuite_con_espacio():
    assert extract_skill_burpsuite("Uso Burp Suite para pruebas web.") == ["Burp Suite"]
 
 
def test_metasploit_simple():
    assert extract_skill_metasploit("Uso Metasploit para explotacion.") == ["Metasploit"]
 
 
def test_pentest_forma_completa():
    assert extract_skill_pentest("Realizo Penetration Testing regularmente.") == ["Penetration Testing"]
 
 
def test_pentest_forma_corta():
    assert extract_skill_pentest("Hago Pentest a aplicaciones web.") == ["Pentest"]
 
 
def test_vulnassessment_simple():
    assert extract_skill_vulnassessment("Realizo Vulnerability Assessment.") == ["Vulnerability Assessment"]
 
 
def test_owasp_simple():
    assert extract_skill_owasp("Sigo la guia OWASP.") == ["OWASP"]
 
 
def test_incidentresponse_simple():
    assert extract_skill_incidentresponse("Participo en Incident Response.") == ["Incident Response"]
 
 
def test_awssecurity_simple():
    assert extract_skill_awssecurity("Manejo AWS Security.") == ["AWS Security"]
 
 
def test_azuresecurity_simple():
    assert extract_skill_azuresecurity("Manejo Azure Security.") == ["Azure Security"]
 
 
def test_git_cyber_simple():
    assert extract_skill_git_cyber("Uso Git para versionar mis scripts.") == ["Git"]
 
 
# ---------- Certificaciones ----------
 
def test_ceh_simple():
    assert extract_skill_ceh("Tengo la certificacion CEH.") == ["CEH"]
 
 
def test_oscp_simple():
    assert extract_skill_oscp("Tengo la certificacion OSCP.") == ["OSCP"]
 
 
def test_securityplus_simple():
    assert extract_skill_securityplus("Tengo la certificacion Security+.") == ["Security+"]
 
 
if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    aprobados = 0
    for test in tests:
        try:
            test()
            print(f"[APROBADO] {test.__name__}")
            aprobados += 1
        except AssertionError as e:
            print(f"[FALLO]    {test.__name__} -> {e}")
    print(f"\n{aprobados}/{len(tests)} tests validos pasados")