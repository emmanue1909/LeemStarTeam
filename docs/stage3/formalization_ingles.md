## Objective 
Classify a resume fragment into one or more of the defined profiles (Full Stack Developer, Cybersecurity Specialist), based on the skills already normalized by Stage 2. Classification is performed using an independent deterministic finite automaton (DFA) per profile. 

## Scope 
- Each profile has its own DFA; they are evaluated independently. A candidate may be accepted by none, one, or $n$ profiles ($p$) where $0 \leq n \leq p$; it is not mutually exclusive. 
- The input to each DFA is the sequence of normalized skills produced by Stage 2 (not raw text). 
- A skill that does not belong to any qualification of the evaluated profile (for example, a Cybersecurity skill when evaluating Full Stack, or an optional certification such as CEH/OSCP/Security+) does nothing: the automaton remains in the same state (self-loop). 
- The order in which skills appear does not affect the outcome; the automaton only accumulates coverage, never losing it. 

## Mapping: skill $\rightarrow$ qualification 
**Full Stack Developer** 

| Qualification        | Skills covering it                          |
| -------------------- | ------------------------------------------- |
| Frontend Development | JavaScript, TypeScript, React, Angular, Vue |
| Backend Development  | Node.js, Django, Spring Boot                |
| Database Management  | SQL, NoSQL                                  |
| API Integration      | APIs REST                                   |
| Version Control      | Git                                         |

**Cybersecurity Specialist** 

| Qualification      | Skills covering it                                                      |
| ------------------ | ----------------------------------------------------------------------- |
| Security Tools     | Nmap, Wireshark, Burp Suite, Metasploit                                 |
| Security Practices | Penetration Testing, Vulnerability Assessment, OWASP, Incident Response |
| Cloud Security     | AWS Security, Azure Security                                            |
| Version Control    | Git                                                                     |

CEH, OSCP, and Security+ do not belong to any qualification (a design decision already established in Stage 1): they appear in Stage 2's output as standalone skills, but do not affect classification. 

## Formal definition 
Each profile is modeled as an independent DFA using the 5-tuple (Q, Σ, δ, q₀, F): 
- **Q** = power set of all possible subsets of the profile's qualifications (each state represents "which qualifications are already covered"). Being a power set, there are 2ⁿ states, where n = number of qualifications in the profile (n=5 for Full Stack → 32 states; n=4 for Cybersecurity → 16 states). Instead of naming each state by the subset it represents (set notation), they are given sequential names q0, q1, ..., q_{2ⁿ−1}, grouped by levels according to how many qualifications they cover (level 0 = none, level n = all). For Cybersecurity (n=4): level 0 → 1 state (q0), level 1 → 4 states (q1..q4), level 2 → 6 states (q5..q10), level 3 → 4 states (q11..q14), level 4 → 1 state (q15). Total: 1+4+6+4+1 = 16 = 2⁴.
- **Σ** = set of all possible normalized skills (those of the profile, those of the other profile, and optional/certifications). 
- **δ** = transition function: δ(S, skill) = S ∪ {qualification(skill)} if *skill* belongs to a qualification of this profile; δ(S, skill) = S otherwise. 
- **q0** = $\emptyset$ (no qualification covered at start), starting at q0. 
- **F** = {Q_total}, where Q_total is the complete set of qualifications for the profile (single acceptance state: full coverage). 

## Acceptance rule
A candidate is classified under a profile if and only if the DFA for that profile, after consuming the entire sequence of normalized skills from the CV, ends in the final state Q_total (that is, it found at least one skill for each of the profile's qualifications). Full Stack and Cybersecurity are evaluated separately under this same rule. 

## Example 
For the Laura Gómez fragment (mySQL, React.js $\rightarrow$ normalized to SQL, REACT): the Full Stack DFA remains in state {Database Management, Frontend Development}, does not reach Q_total (missing Backend, API, Version Control), and is therefore not accepted for that profile with only those two skills.
