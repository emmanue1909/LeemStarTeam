from pyformlang.finite_automaton import DeterministicFiniteAutomaton

from src.data_profiles import PROFILES, SKILL_VARIANTS, vocabulary
from src.emmanuel_bridge import CLASSIFIER

EMMANUEL_AUTOMATA = {'full_stack': CLASSIFIER.dfa_fullstack, 'cybersecurity': CLASSIFIER.dfa_cyber}
LEGACY_SYMBOLS = {
    'POSTGRESQL': 'SQL', 'MYSQL': 'SQL', 'MONGODB': 'NOSQL', 'NODEJS': 'NODE.JS',
    'SPRING_BOOT': 'SPRING BOOT', 'REST_API': 'APIS REST', 'BURP_SUITE': 'BURP SUITE',
    'PENETRATION_TESTING': 'PENETRATION TESTING', 'VULNERABILITY_ASSESSMENT': 'VULNERABILITY ASSESSMENT',
    'INCIDENT_RESPONSE': 'INCIDENT RESPONSE', 'AWS_SECURITY': 'AWS SECURITY',
    'AZURE_SECURITY': 'AZURE SECURITY', 'SECURITY_PLUS': 'SECURITY+',
}


def build_emmanuel_adapter(profile):
    """Preserve the published subset DFA while adapting the shared alphabet."""
    original = EMMANUEL_AUTOMATA[profile]
    labels = {state: str(state.value) for state in original.states}
    alphabet = {str(symbol.value) for symbol in original.symbols}
    adapted = DeterministicFiniteAutomaton()
    for state in original.start_states:
        adapted.add_start_state(labels[state])
    for state in original.final_states:
        adapted.add_final_state(labels[state])
    for state in original.states:
        for token in SKILL_VARIANTS:
            symbol = LEGACY_SYMBOLS.get(token, token)
            target = original(state, symbol)[0] if symbol in alphabet else state
            adapted.add_transition(labels[state], token, labels[target])
    return adapted


def state_coverage(profile):
    """Describe the contributor's sequential state names without renaming them."""
    from itertools import combinations
    original = EMMANUEL_AUTOMATA[profile]
    categories = PROFILES[profile]['categories']
    coverage = {}
    for count in range(len(categories) + 1):
        for indices in combinations(range(len(categories)), count):
            state = next(iter(original.start_states))
            for index in indices:
                token = categories[index][1][0]
                state = original(state, LEGACY_SYMBOLS.get(token, token))[0]
            coverage[str(state.value)] = list(indices)
    return coverage


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
    if profile in EMMANUEL_AUTOMATA:
        return build_emmanuel_adapter(profile)
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
