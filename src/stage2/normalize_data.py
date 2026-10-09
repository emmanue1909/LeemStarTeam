from pyformlang.fst import FST

from src.data_profiles import PROFILES, lexical_token, vocabulary


def build_transducer(profile):
    fst = FST()
    fst.add_start_state("q0")
    fst.add_final_state("q1")
    for canonical, aliases in PROFILES[profile]["variants"].items():
        for alias in aliases:
            fst.add_transition("q0", lexical_token(alias), "q1", [canonical])
    return fst


TRANSDUCERS = {profile: build_transducer(profile) for profile in PROFILES}


def normalize_one(term, profile):
    output = next(TRANSDUCERS[profile].translate([lexical_token(term)]), None)
    return output[0] if output else None


def normalize(terms, profile):
    canonical, unknown = [], []
    for term in terms:
        token = normalize_one(term, profile)
        if token is None:
            unknown.append(term)
        elif token not in canonical:
            canonical.append(token)
    return canonical, unknown


def canonical_order(tokens, profile):
    order = {token: i for i, token in enumerate(vocabulary(profile))}
    return sorted(tokens, key=order.__getitem__)
