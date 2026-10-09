from pyformlang.finite_automaton import DeterministicFiniteAutomaton

from src.data_profiles import PROFILES, vocabulary


def next_state(state, token, profile):
    if state == "q_dead":
        return state
    i = int(state[1:])
    groups = [tokens for _, tokens in PROFILES[profile]["categories"]]
    if i < len(groups) and token in groups[i]:
        return f"q{i + 1}"
    if i > 0 and token in groups[i - 1]:
        return state
    return "q_dead"


def build_automaton(profile):
    dfa = DeterministicFiniteAutomaton()
    k = len(PROFILES[profile]["categories"])
    states = [f"q{i}" for i in range(k + 1)] + ["q_dead"]
    for state in states:
        for token in vocabulary(profile):
            dfa.add_transition(state, token, next_state(state, token, profile))
    dfa.add_start_state("q0")
    dfa.add_final_state(f"q{k}")
    return dfa


AUTOMATA = {profile: build_automaton(profile) for profile in PROFILES}


def classify(tokens, profile):
    dfa = AUTOMATA[profile]
    state, trace = "q0", []
    for token in tokens:
        destinations = dfa(state, token)
        target = str(destinations[0].value) if destinations else "q_dead"
        trace.append({"from": state, "symbol": token, "to": target})
        state = target
    missing = [name for name, group in PROFILES[profile]["categories"] if not set(group).intersection(tokens)]
    return {"accepted": dfa.accepts(tokens), "missing_categories": missing, "trace": trace}
