import sys
from pathlib import Path
 
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
 
from src.stage1.extract_specific import (
    extract_skill_javascript, extract_skill_typescript, extract_skill_react,
    extract_skill_angular, extract_skill_vue, extract_skill_nodejs,
    extract_skill_django, extract_skill_sql, extract_skill_nosql,
    extract_skill_apis_rest, extract_skill_git,
    extract_qualifications_frontend_fullstack, extract_qualifications_backend_fullstack,
    extract_qualifications_database_fullstack, extract_qualifications_versioncontrol_fullstack,
    extract_qualifications_securitytools_cyber, extract_qualifications_securitypractices_cyber,
    extract_qualifications_cloudsecurity_cyber,
    extract_skill_nmap, extract_skill_wireshark, extract_skill_burpsuite,
    extract_skill_metasploit, extract_skill_pentest, extract_skill_vulnassessment,
    extract_skill_owasp, extract_skill_incidentresponse, extract_skill_awssecurity,
    extract_skill_azuresecurity, extract_skill_git_cyber,
    extract_skill_ceh, extract_skill_oscp, extract_skill_securityplus,
)
 
 
# ---------- Skills Full Stack ----------
 
def test_javascript_ausente():
    assert extract_skill_javascript("No menciono lenguajes de frontend.") == []
 
 
def test_javascript_no_falso_positivo_en_frameworks_js():
    """Node.js / React.js no deben contarse como mencion de JavaScript suelto."""
    assert extract_skill_javascript("Trabajo con Node.js y React.js.") == []
 
 
def test_typescript_ausente():
    assert extract_skill_typescript("No uso tipado estricto.") == []
 
 
def test_react_ausente():
    assert extract_skill_react("No uso frameworks de frontend.") == []
 
 
def test_angular_ausente():
    assert extract_skill_angular("No trabajo con frameworks de UI.") == []
 
 
def test_vue_ausente():
    assert extract_skill_vue("No manejo frameworks de UI.") == []
 
 
def test_nodejs_ausente():
    assert extract_skill_nodejs("El backend esta en Python.") == []
 
 
def test_django_ausente():
    assert extract_skill_django("Uso Flask para el backend.") == []
 
 
def test_sql_ausente():
    assert extract_skill_sql("La base de datos es no relacional.") == []
 
 
def test_nosql_ausente():
    assert extract_skill_nosql("Uso una base de datos relacional.") == []
 
 
def test_apis_rest_ausente():
    assert extract_skill_apis_rest("No diseno servicios web.") == []
 
 
def test_git_no_matchea_dentro_de_gitlab():
    """Confirma que el \\b evita falsos positivos de "Git" dentro de "Gitlab"."""
    assert extract_skill_git("Publico mis proyectos en Gitlab.") == []
 
 
# ---------- Qualifications Full Stack ----------
 
def test_qualification_frontend_fuera_de_rango_6():
    assert extract_qualifications_frontend_fullstack("Tengo un nivel 6 en Frontend Development.") == []
 
 
def test_qualification_backend_fuera_de_rango_0():
    assert extract_qualifications_backend_fullstack("Tengo un nivel 0 en Backend Development.") == []
 
 
def test_qualification_database_ausente():
    assert extract_qualifications_database_fullstack("No menciono mi nivel en bases de datos.") == []
 
 
def test_qualification_versioncontrol_fullstack_ausente():
    assert extract_qualifications_versioncontrol_fullstack("Tengo experiencia en control de versiones.") == []
 
 
# ---------- Qualifications Cybersecurity ----------
 
def test_qualification_securitytools_fuera_de_rango_9():
    assert extract_qualifications_securitytools_cyber("Tengo un nivel 9 en Security Tools.") == []
 
 
def test_qualification_securitypractices_ausente():
    assert extract_qualifications_securitypractices_cyber("No menciono mis practicas de seguridad.") == []
 
 
def test_qualification_cloudsecurity_ausente():
    assert extract_qualifications_cloudsecurity_cyber("Tengo un nivel 4 en seguridad en general.") == []
 
 
# ---------- Skills Cybersecurity ----------
 
def test_nmap_ausente():
    assert extract_skill_nmap("Uso herramientas de escaneo.") == []
 
 
def test_wireshark_ausente():
    assert extract_skill_wireshark("Analizo trafico de red.") == []
 
 
def test_burpsuite_ausente():
    assert extract_skill_burpsuite("Uso herramientas de pruebas web.") == []
 
 
def test_metasploit_ausente():
    assert extract_skill_metasploit("Uso tecnicas de explotacion.") == []
 
 
def test_pentest_ausente():
    assert extract_skill_pentest("Realizo auditorias de seguridad.") == []
 
 
def test_vulnassessment_ausente():
    assert extract_skill_vulnassessment("Realizo evaluaciones de seguridad.") == []
 
 
def test_owasp_ausente():
    assert extract_skill_owasp("Sigo buenas practicas de seguridad.") == []
 
 
def test_incidentresponse_ausente():
    assert extract_skill_incidentresponse("Participo en gestion de riesgos.") == []
 
 
def test_awssecurity_ausente():
    assert extract_skill_awssecurity("Manejo seguridad en la nube.") == []
 
 
def test_azuresecurity_ausente():
    assert extract_skill_azuresecurity("Manejo infraestructura en la nube.") == []
 
 
def test_git_cyber_no_matchea_dentro_de_gitlab():
    assert extract_skill_git_cyber("Publico mis scripts en Gitlab.") == []
 
 
# ---------- Certificaciones ----------
 
def test_ceh_ausente():
    assert extract_skill_ceh("Tengo certificaciones de seguridad.") == []
 
 
def test_oscp_ausente():
    assert extract_skill_oscp("Tengo certificaciones ofensivas.") == []
 
 
def test_securityplus_ausente():
    assert extract_skill_securityplus("Tengo certificaciones variadas.") == []
 
 
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
    print(f"\n{aprobados}/{len(tests)} tests invalidos pasados")