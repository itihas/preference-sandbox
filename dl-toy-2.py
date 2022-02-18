# dl-toy-2.py

# Player: Sym
# Property:: Sym
# PPref:: Poset Property
# Outcome:: Set Property
# OPref :: Poset Outcome
# le :: Poset a => a -> a -> Bool
# lt :: Poset a => a -> a -> Bool
# gt :: Poset a => a -> a -> Bool
# incmp :: Poset a => a -> a -> Bool
# maximals :: Poset a => Set a -> Set a
# maximals coll = filter (\x: not any le x coll) coll
# minimals :: Poset a => Set a -> Set a
# minimals coll = filter (\x: not any ge x coll) coll
# PPrefMap:: Player -> PPref
# MotivState:: Set Property
# MotivStateMap:: Player -> MotivState
# PossibleMotivStates:: Set MotivState
# PossibleMotivStatesMap:: Player -> PossibleMotivStates
# Assignment:: PossibleMotivStates -> MotivState
# assign: Assignment -> PossibleMotivStatesMap -> MotivStateMap
# assign assgnmnt pmsmap = assgnmnt . pmsmap
# assign = (.)
# salientPPref :: MotivState -> PPref -> PPref
# salientPPref ms ppr  = intersection ms ppr
# salientPPref = intersection
# prefPToO :: PPref -> Set Outcome -> OPref
# prefPToO ppr os = for x1,x2 in os*os, add x to returns if forall y1 in x1, y2 in x2, y1 <= y2
# prefPToO ppr os = filter (\o1 o2 . (any leq o1*o2)) os*os
# paretoMaximals :: OPrefMap -> Set Outcome
# paretoMaximals oprm players outcomes = for o in outcomes, for p in players, if (o,_) in oprm p, remove 0
# paretoMaximals oprm players outcomes = filter (\o . not (for p in players, o in minimals oprm p)) outcomes

import itertools


# smol relation system
# feed this with irreflexive orderings and it will still assume reflexive elements are present
# write this into constructor and take it out of predicates later
def leq(rel, x1, x2): return (x1, x2) in rel
def geq(rel, x1, x2): return (x2, x1) in rel

def eq(rel, x1, x2): return x1 == x2
def cmpble(rel, x1, x2): return leq(rel, x1, x2) or geq(rel, x1, x2)
def incmpble(rel, x1, x2): return not cmpble(rel,x1,x2)

def rel_set(rel):
    s = set()
    {s.update(x) for x in rel}
    return s

def maximals(rel):
    pss = rel_set(rel)
    return {i for i in pss if all ([incmpble(rel,i,j) or geq(rel, i, j) for j in pss])}

def indiffs(rel,alts):
    pss = rel_set(rel)
    return {i for i in alts if all ([incmpble(rel,i,j) for j in pss])}

def minimals(rel):
    pss = rel_set(rel)
    return {i for i in pss if all ([incmpble(rel,i,j) or leq(rel, i, j) for j in pss])}


def assign(possible_motiv_states_map, assignment):
    return {k:v[assignment[k]] for k,v in possible_motiv_states_map.items()}

# motivational states are a topology
# =====
# what we want is for each value in possible_motiv_states to be a topology over properties, i.e. for it to obey the following axioms:
# 1. all_props in pms and {} in pms
# 2. if a in pms and b in pms: union(a,b) in pms
# 3. if a in pms and b in pms: intersection(a,b) in pms
# sooo, we can construct a pms obeying these as a closure over any pms - add in the unions, intersections, all_props, and empty.
# which is what we'll do, because it's easy.
# the question still remains: which of these is _interesting_?


def top_closure(pms, props):
    additions = [props, set()]
    for ms in pms:
        for ms1 in pms:
            additions.append(set.union(ms,ms1))
            additions.append(set.intersection(ms,ms1))
    return set.union(pms,frozenset(additions))


def salient_ppref(motiv_state, ppref):
    return filter((lambda x: x[0] in motiv_state and x[1] in motiv_state),ppref)


def pref_p_to_o(ppref, outcomes):
    print("\tp_to_o:\n\t\tppref:",ppref,"\n\t\tresult:",{(x,y):all([incmpble(ppref, i,j) or leq(ppref,i,j) for i in outcomes[x] for j in outcomes[y]]) for x in outcomes for y in outcomes})
    return {(x,y) for x in outcomes for y in outcomes if all([incmpble(ppref, i,j) or leq(ppref,i,j) for i in outcomes[x] for j in outcomes[y]])}


def pareto_dominants(prefmap, alts, alt):
    ret = {alt1 for alt1 in alts if alt != alt1 and all([leq(pref, alt, alt1) for pref in prefmap.values()])}
    print("\tdominants:", alt, "<=",ret)
    return ret

def pareto_front(prefmap, alts):
    print("\tfront:", prefmap, "\n\talts:",alts)
    return {a for a in alts if not pareto_dominants(prefmap,alts,a)}


# Fix (possible) motivational states, derive prefs
# ====
# given a motivational state and an set of properties, output a candidate preference.
# given a motivational state and a set of outcomes, say whether there exist preferences over properties that can distinguish outcomes.
#  \-> for this we need: given a set of outcomes, say whether there exist preferences over properties that can distinguish those outcomes.

def distinguish_outcomes(o1, o2):
    return {(p1,p2) for p1 in o1 for p2 in o2 if p1 != p2}

def distinguishable_outcomes(motiv_state, outcomes):
    return {distinguish_outcomes(o1,o2) is not None for o1 in outcomes for o2 in outcomes}

def distinguish_outcomes_modulo_salience(motiv_state, o1, o2):
    return {(p1,p2) for p1 in o1 for p2 in o2 if p1 != p2 and p1 in motiv_state and p2 in motiv_state}

def distinguishable_outcomes_under_salience(motiv_state, outcomes):
    return {distinguish_outcomes_modulo_salience(motiv_states,o1,o2) is not None for o1 in outcomes for o2 in outcomes}

def all_salient_ppref_candidates(motiv_state, outcomes):
    candidates = set()
    [candidates.union(distinguish_outcomes_modulo_salience(motiv_states,o1,o2)) for o1 in outcomes for o2 in outcomes]
    return candidates

# finding all posets that fulfil the salience criteria, by building them out of the candidate relations.
# might not be the most efficient way.
def possible_salient_pprefs(motiv_state,outcomes,curr):
    aspc = all_salient_ppref_candidates(motiv_state,outcomes)
    possibles = [curr]
    for p in aspc:
        if p not in curr and p[::-1] not in curr:
            possibles.extend(possible_salient_pprefs(motiv_state, outcomes, curr.add(p)))
    return possibles


# going by sequence for number-of-posets (https://oeis.org/A001035) this is likely to get out of hand to generate very quickly. But if we establish an order over the preference_candidates (which we can get out of an order over the preferences, ofc), we get a lex order over the posets also; and can probably generate the poset associated with a given index. (Uniquely identifying posets by number is kinda cool and seems useful anyway.)
# Question: just how much smaller than the total number of posets is the number of salient pprefs? How much does the motiv-state business narrow things down?
# It's more than the number of posets over the set of distinguishable outcomes, but less than the number of posets over the set of salient properties. (Latter because there are some property distinctions that are not useful for distinguishing outcomes.)
# oh, also: how many properties at minimum do you need to distinguish between n outcomes?
# conversely: given a motiv_state (i.e. a set of salient properties) of size n, what is the largest number of outcomes that we can distinguish between?
# ugh this has the flavor of number theory
# I hate it already
# i.e. the largest number of unique subsets of n.
# oh that's simpler. that's just 2^n.
# OH WAIT SHIT TRANSITIVITY
# okay now we need that data structure for posets there's no way around it
# hmm siena poset: transitive relationships are _implied_.
# problem here: we gotta do "build one viable poset" before we get "generate all viable posets"



def main():
    sample_properties = set("abcd")
    sample_players = ["Alice", "Bob"]
    # sample_outcomes = {"alpha":frozenset("a"), "gamma":frozenset("b")}
    sample_outcomes = {"alpha":frozenset("a"), "gamma":frozenset("bc")}

    sample_ppref = {("a", "b"), ("b", "c")}
    sample_pprefmap = {"Alice":{("a","b"), ("b", "c"), ("c", "a")}, "Bob":{("a", "b")}}
    # sample_pprefmap = {"Alice":{("a","b"), ("b", "c"), ("c", "d"), ("d", "a")}, "Bob":{("a", "b")}}

    sample_motiv_state = {"b", "c"}
    sample_motiv_state_map = {"Alice":{"a", "b", "c"}, "Bob": {"a", "b"}}

    sample_possible_motiv_states = [["a", "b", "c"], ["a", "b"], ["c", "b", "d"]]
    sample_possible_motiv_states_map = {"Alice": [["a", "b", "c"], ["a", "b"]], "Bob": [["a", "b"],  ["c", "b", "d"]]}

    sample_assignment = {"Alice": 1, "Bob":0}


    print("\nleq_test:", leq(sample_ppref, "a", "b"))
    print("maximals_test:", maximals(sample_ppref))
    print("indiffs_test:", indiffs(sample_ppref,sample_properties))
    print("sample_possible_motiv_states_map: ", sample_possible_motiv_states_map)
    print("sample_assignment: ", sample_assignment)
    derived_msm = assign(sample_possible_motiv_states_map,sample_assignment)
    print("derived_motiv_states_map: ", derived_msm)
    print("sample_motiv_state:", sample_motiv_state)
    derived_salient_ppref = list(salient_ppref(sample_motiv_state, sample_ppref))
    print("sample_ppref:", sample_ppref, "\nderived_salient_ppref:", derived_salient_ppref)
    derived_salient_pprefmap = {player:set(salient_ppref(derived_msm[player] , ppref)) for player,ppref in sample_pprefmap.items()}
    print("sample_pprefmap:", sample_pprefmap, "\nderived_salient_pprefmap:", derived_salient_pprefmap)
    derived_oprefmap = {player:set(pref_p_to_o(ppref, sample_outcomes)) for player,ppref in derived_salient_pprefmap.items()}
    print("derived_oprefmap:", derived_oprefmap)
    print("pareto_dominants:", pareto_dominants(sample_pprefmap, sample_properties, "d" ))
    print("pareto_front__sample_pprefs:", pareto_front(sample_pprefmap, sample_properties))
    print("pareto_front__pprefs:", pareto_front(derived_salient_pprefmap, sample_properties))
    print("pareto_front__oprefs:", pareto_front(derived_oprefmap, sample_outcomes))
    

    
main()
