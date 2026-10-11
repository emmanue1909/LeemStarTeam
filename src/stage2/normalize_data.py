from pyformlang.fst import FST

from src.data_profiles import PROFILES, SKILL_VARIANTS, QUALIFICATION_VARIANTS, lexical_token, vocabulary


def transducer_from_variants(variants):
    fst = FST()
    fst.add_start_state("q0")
    fst.add_final_state("q1")
    for canonical, aliases in variants.items():
        for alias in aliases:
            fst.add_transition("q0", lexical_token(alias), "q1", [canonical])
    return fst


def build_transducer(profile):
    return transducer_from_variants(PROFILES[profile]['variants'])


TRANSDUCERS = {profile: build_transducer(profile) for profile in PROFILES}
SKILL_TRANSDUCER = transducer_from_variants(SKILL_VARIANTS)
QUALIFICATION_TRANSDUCER = transducer_from_variants(QUALIFICATION_VARIANTS)


def translate_one(term, fst):
    output = next(fst.translate([lexical_token(term)]), None)
    return output[0] if output else None


def normalize_skills(terms):
    tokens, unknown = [], []
    for term in terms:
        token = translate_one(term, SKILL_TRANSDUCER)
        if token is None:
            unknown.append(term)
        elif token not in tokens:
            tokens.append(token)
    return tokens, unknown


def normalize_qualifications(declarations):
    normalized, errors, seen = [], [], {}
    for item in declarations:
        if isinstance(item, (tuple, list)) and len(item) == 2:
            level, term = item
        elif isinstance(item, dict):
            term, level = item.get('term', item.get('name')), item.get('level')
        else:
            errors.append('Malformed qualification declaration')
            continue
        if not isinstance(term, str) or not isinstance(level, (int, str)) or isinstance(level, bool):
            errors.append('Malformed qualification declaration')
            continue
        try:
            level = int(level)
        except ValueError:
            errors.append('Invalid declared level: ' + str(level))
            continue
        token = translate_one(term, QUALIFICATION_TRANSDUCER)
        if token is None:
            errors.append('Unknown qualification: ' + term)
            continue
        if not 1 <= level <= 5:
            errors.append('Declared level outside 1..5: ' + token)
        if token in seen:
            if seen[token] != level:
                errors.append('Conflicting declared levels: ' + token)
        else:
            normalized.append({'name': token, 'level': level})
            seen[token] = level
    return normalized, errors


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
