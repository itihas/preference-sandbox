# dl-toy.py

# game states possess properties, game players prefer over properties in a poset (DAG)
# players only ever express (decide using) preferences over outcomes, using a "motivationally salient" subset of properties
# WHEN does a given motivationally salient subset become active?



properties = ["a", "b"] #, "c", "d"]

# Outcomes : Set Set Property
# outcomes = [(properties*2)[i:i+2] for i in range(len(properties))]

outcomes = [["a"],["a" ,"b"]]

players = ["Alice", "Bob"] #, "Claire"]


# Preference : Poset Property
# PreferenceMap : Player -> Preference

# preferences = {players[i]:[(properties*2)[j:j+2] for j in range(i+2,i+4)] for i in range(len(players))}
# preferences = {players[i]:[((properties*2)[j], (properties*2)[k]) for (j,k) in [(i,i+1), (i+1,i+2), (i+2,i)]] for i in range(len(players))}
preferences = {"Alice":[("a","b")], "Bob":[("a", "b")]}

# MS : Set Property
# PMS : Player -> Set MS

possible_motiv_states = {players[i]:[(properties*2)[j:j+3] for j in [i+1, i+3]] for i in range(len(players))}



print(properties)
print(outcomes)
print(players)
print(preferences)
print(possible_motiv_states)


# assign_MS: PMS -> Assignment -> (Player -> MS)
# assign_MS: (Player -> Set MS) -> Assignment -> Player -> MS
# Bad way to configure


# salient_prefs: Assignment -> ____? -> PreferenceMap
def salient_prefs(assignment):
    
    # motiv_states = {i:possible_motiv_states[i][j] for i in players for j in assignment}
    motiv_states = {k:v[j] for (k,v),j in zip(possible_motiv_states.items(), assignment)}
    print("motiv_states", motiv_states)

    return {i:[(j,k) for (j,k) in preferences[i] if j in motiv_states[i] and k in motiv_states[i]] for i in players}



print("salient prefs",salient_prefs([0,0,0]))


# outcome_ge: Outcome -> Outcome -> Preference -> Bool

def outcome_ge(outcome1, outcome2, prop_prefs):
    for o1 in outcome1:
        for o2 in outcome2:
            if (o2,o1) in prop_prefs:
                return False
    return True
        
# OPref : Poset Outcome
# OPrefMap : Player -> OPref
# outcome_prefs: PreferenceMap -> Outcomes -> OPrefMap
def outcome_prefs(prefs):
    return {k: 
             [(j,k) for j in range(len(outcomes)) for k in range(len(outcomes)) if not outcome_ge(outcomes[k], outcomes[j], v)]
            for k,v in prefs.items()}


print(outcome_prefs(salient_prefs([0,0,0])))

# pareto_maximal_outcomes: OPrefMap -> Set Outcome
def pareto_maximal_outcomes(oprefs):
    discards = set()
    all_prefs = [i for j in oprefs.values() for i in j]
    for i in range(len(outcomes)):
        for j in range(len(outcomes)):
            if i != j and (i,j) in all_prefs:
                discards.add(i)
    print(discards)
    return set(range(len(outcomes))) - discards

print(pareto_maximal_outcomes(outcome_prefs(salient_prefs([0,0,0]))))
