Before defining regex patterns, the scoping decisions made by the team are documented (following the same approach as `decisiones.md` in Stage 4):

## Objective 
Extract raw resume information (contact, languages, frameworks, databases, experience, certifications, etc.) using Python's `re` module as input for Stage 2 (FST normalization).

## Common scopes

- **Email:** not restricted to specific providers (Gmail, Yahoo, Outlook). Only the general structure `user@domain.tld` is validated, to also accept corporate or institutional emails (e.g., `@icesi.edu.co`). Example: 'camila.redondo@gmail.com'

- **Phone:** fixed format of 3 hyphen-separated groups: `+<country_code>-<city_code>-<number>` (e.g., `+57-4-5559876`). Other formats are not considered (mobile phones without city code, spaces instead of hyphens, etc.), because that is how the format is handled in the examples and as decided. Example: '+57-4-5559876'

- **Years of experience**: range (0, 60), excluding the endpoints — that is, values between 1 and 59. This range must match the one already validated by `validator.py` in Stage 4 to maintain consistency across the entire pipeline. With this in mind, we will use the anchor phrase: "mi experiencia es de `<years>` años". Example: "mi experiencia es de 20 años"

- **Name:** string of minimum 2 and maximum 4 space-separated words (e.g., "Juan Pérez" with 2, or "Sandra Lorena Muñoz Vela" with 4), covering the usual combinations of given name(s) + surname(s) in Colombia. Names of 5 or more words are not considered. Using the anchor phrase "mi nombre es `<name>`". Example: "mi nombre es Juan Pérez"
- **Location**: To locate the candidate, we will filter by words surrounding the part of interest since there is no fixed format to extract city and country; with these anchor phrases we can extract them such that: "radicada/radicado en `<location>`". Example: "radicada en Cali, Colombia" -> location = "Cali, Colombia".
- **GitHub**: For the GitHub user handle, it can be optional and in this case we also lack a fixed format for the GitHub user, so we will also use anchor phrases like: "usuario de GitHub es `<github>`". Example: "usuario de GitHub es lauragomez" -> github = "lauragomez".
- **Position + Company**: This case is slightly more complex, lacking a fixed structure and with less specific anchor phrases, but we will adopt the simplified case such that: "mi posicion es `<position>` en la compañia`<company>`". Example: "mi posicion es Security Engineer en la compañia Globant" -> position = "Security Engineer", company = "Globant".
- **Institution + Program**: For this case the same applies as mentioned previously, so we will use the anchor phrase: "egresada/egresado del programa de `<program>` de la `<institution>`". Example: "egresada del programa de Ingeniería de Sistemas de la Universidad Icesi" 

**NOTE:** Anchor phrases that include participles ("radicada/radicado", "egresada/egresado") must accept both endings (`radicad[oa]`, `egresad[oa]`), as candidate examples may be male or female.

## Expressions by profile

**Skills and qualifications (all profiles):** detection is case-insensitive — "react", "React", and "REACT" count as the same match, provided it matches a skill from the known list.

**Design note:** for an example to count as "valid" for a profile, merely mentioning several skills is not sufficient — the candidate must cover all categories of that profile (see the minimum acceptance rule defined in `docs/stage3_automata/formalizacion.md`). This affects how example paragraphs for this stage are drafted.

## PROFILES
### Full Stack Developer
#### Skills (specific, without level) 
- JavaScript 
- TypeScript
- React
- Angular
- Vue
- Node.js
- Django
- Spring Boot
- SQL 
- NoSQL
- APIs REST
- Git 
#### Qualifications (domain areas, with level 1-5)
- Frontend Development
- Backend Development
- Database Management
- API Integration
- Version Control

**NOTE:** For qualifications, to retrieve their level since it is an integer, we will use an anchor phrase: "tengo un nivel `<level>` en `<qualification>`". Example: "tengo un nivel 4 en Frontend Development".

### Cybersecurity Specialist 
#### Skills (specific, without level)
- Nmap 
- Wireshark
- Burp Suite
- Metasploit
- Penetration Testing
- Vulnerability Assessment
- OWASP
- Incident Response
- AWS Security
- Azure Security
- Git
- CEH
- OSCP
- Security+ 
#### Qualifications (domain areas, with level 1-5)
- Security Tools
- Security Practices
- Cloud Security
- Version Control

**NOTE:** CEH, OSCP, and Security+ are certifications and are not grouped under any qualification — they are extracted as normal skills but are optional: they do not count toward any category of the minimum acceptance rule (see `docs/stage3_automata/formalizacion.md`), unlike other skills that do belong to one of the 4 qualifications (Security Tools, Security Practices, Cloud Security, Version Control). Similarly, for qualifications, to retrieve their level since it is an integer, we will use an anchor phrase: "tengo un nivel `<level>` en `<qualification>`"

## Recognized abbreviations and variants

In addition to case-insensitive detection, real-world variants frequently found in resumes are considered for each skill. Stage 1 captures raw text exactly as it appears (the variant), and Stage 2 (FST) normalizes it to the canonical form — see `docs/stage2_fst/formalizacion.md`.

### Full Stack Developer

| Skill (canonical) | Recognized variants                        |
| ----------------- | ------------------------------------------ |
| JavaScript        | JavaScript, Java Script, JS                |
| TypeScript        | TypeScript, Type Script, TS                |
| React             | React, React.js, ReactJS                   |
| Angular           | Angular, AngularJS                         |
| Vue               | Vue, Vue.js, VueJS                         |
| Node.js           | Node.js, Node, NodeJS                      |
| Django            | Django                                     |
| Spring Boot       | Spring Boot, SpringBoot                    |
| SQL               | SQL, MySQL, PostgreSQL, Postgres           |
| NoSQL             | NoSQL, MongoDB, Mongo                      |
| APIs REST         | APIs REST, API REST, REST API, RESTful API |
| Git               | Git                                        |

### Cybersecurity Specialist

| Skill (canonical) | Recognized variants |
|---|---|
| Nmap | Nmap, Network Mapper |
| Wireshark | Wireshark |
| Burp Suite | Burp Suite, BurpSuite, Burp |
| Metasploit | Metasploit, Metasploit Framework |
| Penetration Testing | Penetration Testing, Pentesting, PenTest, Pentest |
| Vulnerability Assessment | Vulnerability Assessment |
| OWASP | OWASP, Open Web Application Security Project |
| Incident Response | Incident Response |
| AWS Security | AWS Security, Amazon Web Services Security |
| Azure Security | Azure Security, Microsoft Azure Security |
| Git | Git |
| CEH | CEH, Certified Ethical Hacker |
| OSCP | OSCP, Offensive Security Certified Professional |
| Security+ | Security+, CompTIA Security+ |

## Design decisions — scope of variants

- **Spring Boot**: "Spring" alone is not considered a variant — it is also a common word (the season, a spring), and accepting it alone would risk false positives.
- **Git**: GitHub and GitLab are not considered variants — they are hosting platforms, not the version control tool itself; they are related but distinct concepts.
- **AWS Security / Azure Security**: "AWS" or "Azure" alone are not considered — someone can have experience in those cloud providers without it being specifically security-related, and accepting them alone would misclassify that experience as the security skill.
