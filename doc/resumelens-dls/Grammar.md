## 3. Language design

```mermaid
graph LR
    Resume --> PersonalInfo
    PersonalInfo --> name
    PersonalInfo --> location
    Resume --> Contact
    Contact --> email
    Contact --> github
    Resume --> Experience
    Experience --> position
    Experience --> company
    Experience --> years
    Resume --> Education
    Education --> institution
    Education --> phone
    Education --> program
    Resume --> Skills
    Skills --> Python
    Skills --> Pandas
    Skills --> SQL
    Resume --> Qualification
    Qualification --> qualname["nombre"]
    Qualification --> level
    Resume --> Classification
    Classification --> MLEngineer["ML Engineer"]
```


## 4. EBNF specification

### 4.1 Terminals

	STRING  
	INT
	"name" 
	"location" 
	"email"
	"github" 
	"position" 
	"company" 
	"years" 
	"institution" 
	"phone" 
	"program" 
	"skill" 
	"qualification" 
	"level" 
	"classification"
	"Machine Learning Engineer" 
	"Full Stack Developer" 
	"Cybersecurity Specialist" 
	"Software Architect"

### 4.2 Non Terminals
	
	Resume 
	PersonalInfo 
	Contact 
	Experience 
	Education 
	Skill 
	Qualification 
	Classification
	AcceptedProfile
	Name
	Location
	Email
	Github
	Position
	Company
	Years
	InstitutionName 
	Phone
	ProgramS

### 4.3 EBNF rules
	Resume ::= PersonalInfo Contact Experience+ Education+ Skill+ Qualification+ Classification+
	PersonalInfo ::= "name" Name "location" Location 
	Contact ::= "email" Email [ "github" Github ] 
	Experience ::= "position" Position "company" Company "years" Years
	Education ::= "institution" InstitutionName "phone" Phone "program" Program
	Skill ::= "skill" STRING 
	Qualification ::= "qualification" STRING "level" INT
	Classification ::= "classification" AcceptedProfile 
	AcceptedProfile ::= "Machine Learning Engineer" | "Full Stack Developer" | "Cybersecurity Specialist" | "Software Architect"
	Name ::= STRING
	Location ::= STRING
	Email ::= STRING
	Github ::= STRING
	Position ::= STRING
	Company ::= STRING
	Years ::= INT
	InstitutionName := STRING 
	Phone := STRING 
	Program := STRING
