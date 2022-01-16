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

def salient_ppref(motiv_state, ppref):
    return filter((lambda x: x[0] in motiv_state and x[1] in motiv_state),ppref)

def pref_p_to_o(ppref, outcomes):
    print("p_to_o: ppref",ppref,"\nresult",{(x,y):all([incmpble(ppref, i,j) or leq(ppref,i,j) for i in outcomes[x] for j in outcomes[y]]) for x in outcomes for y in outcomes})
    return {(x,y) for x in outcomes for y in outcomes if all([incmpble(ppref, i,j) or leq(ppref,i,j) for i in outcomes[x] for j in outcomes[y]])}


def pareto_maximals(prefmap, alts):
    return {a for a in alts if any([a in maximals(prefs) for prefs in prefmap.values()]) and all([a in maximals(prefs) or a in indiffs(prefs,alts) for prefs in prefmap.values()])}





def main():
    sample_properties = set("abcd")
    sample_players = ["Alice", "Bob"]
    # sample_outcomes = {"alpha":frozenset("a"), "gamma":frozenset("b")}
    sample_outcomes = {"alpha":frozenset("a"), "gamma":frozenset("bc")}

    sample_ppref = {("a", "b"), ("b", "c")}
    sample_pprefmap = {"Alice":{("a","b"), ("b", "c"), ("c", "a")}, "Bob":{("a", "b")}}
    # sample_pprefmap = {"Alice":{("a","b"), ("b", "c"), ("c", "d"), ("d", "a")}, "Bob":{("a", "b")}}

    sample_motiv_state = {"a", "b", "c"}
    sample_motiv_state_map = {"Alice":{"a", "b", "c"}, "Bob": {"a", "b"}}

    sample_possible_motiv_states = [["a", "b", "c"], ["a", "b"], ["c", "b", "d"]]
    sample_possible_motiv_states_map = {"Alice": [["a", "b", "c"], ["a", "b"]], "Bob": [["a", "b"],  ["c", "b", "d"]]}

    sample_assignment = {"Alice": 0, "Bob":0}


    
    print("maximals test", maximals(sample_ppref))
    print("indiffs test", indiffs(sample_ppref,sample_properties))
    msm = assign(sample_possible_motiv_states_map,sample_assignment)
    print("motiv state selection test", msm)
    sample_salient_ppref = list(salient_ppref(sample_motiv_state, sample_ppref))
    print("pprefs", sample_ppref, "\nsalient pprefs", sample_salient_ppref)
    salient_pprefmap = {player:set(salient_ppref(msm[player] , ppref)) for player,ppref in sample_pprefmap.items()}
    print("ppref map", sample_pprefmap, "\nsalient ppref map", salient_pprefmap)
    oprefmap = {player:set(pref_p_to_o(ppref, sample_outcomes)) for player,ppref in salient_pprefmap.items()}
    print("opref map", oprefmap)
    pm = pareto_maximals(oprefmap, sample_outcomes)
    print("pareto maximals - pprefs", set(pareto_maximals(salient_pprefmap, sample_properties)))
    print("pareto maximals - oprefs", set(pm))

    
main()
