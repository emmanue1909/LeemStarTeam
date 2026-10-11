## Objective 
Normalize the skill and qualification variants extracted raw by Stage 1 (e.g., "mySQL", "JS", "Pentest") into their unique canonical form (e.g., "SQL", "JavaScript", "Penetration Testing"), so that Stage 3 can classify against a closed and consistent list. 

## Scope 
Only skills and qualifications are normalized. The 8 common fields (email, phone, name, etc.) are already produced in their final form by Stage 1 and do not pass through this transducer. 

## Formal definition
Each skill/qualification is modeled as an independent finite state transducer using the 7-tuple (Q, Σ, Γ, δ, σ, q₀, F): 
- **Q** = {q0, qf}  two states: the initial state and the acceptance state. 
- **Σ** = set of recognized variants for that skill/qualification (input alphabet). E.g., for SQL: {SQL, MySQL, PostgreSQL, Postgres}. 
- **Γ** = {canonical name} output alphabet, a single symbol (e.g., {SQL}). 
- **δ** = transition function: δ(q₀, variant) = qf, for every variant ∈ Σ. 
- **σ** = output function: σ(q₀, variant) = canonical name, for every variant ∈ Σ. 
- **F** = {qf}. 
In other words: each transducer receives as a complete input one of the recognized variants (the raw text extracted by Stage 1) and, in a single transition, produces the corresponding canonical name. There are no intermediate states because the variant is consumed as a single atomic symbol (the complete word), not character by character. 

## Normalization maps 
The canonical → variants tables for each skill/qualification are already documented in `docs/stage1_regex/formalizacion.md`, section "Recognized abbreviations and variants". Stage 2 reuses those same tables (inverted to canonical → [variants]) to build the transducers, so they are not duplicated here. 

**Note on qualifications:** Qualifications have no recognized variants (they are already extracted with their full name, by decision of Stage 1), so their transducer is trivial: Σ = {full name} = Γ, meaning δ and σ map the single input to itself. They are modeled identically with the 7-tuple for formal consistency with skills, although in practice they do not normalize anything.
