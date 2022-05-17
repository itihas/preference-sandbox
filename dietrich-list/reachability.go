package main

import (
	"fmt"
	"io/ioutil"
	"strings"
	"github.com/dghubble/trie"
)

func main() {
	fmt.Println("Dietrich-List Reachability Game")
}


// We have to reimplement all the base machinery here, which means we can /improve/ it hopefully.
// How Posets? Seriously tho. (Probably a Hasse diagram as a map. Simplest way.)
// How do we check that a map is a legal Hasse diagram? (Well, we check for cycles, like the typical DP problem would have us do.)

// Game states are int, all states are "alternatives" i.e. can be preferred or dispreferred.

type edge struct {
	from, to int
}

type gameboard struct {
	edges map[edge]bool 	// state1 < state2 iff state2 in prefs[state1]
	point int
}


// Under reachability, properties are just claims about what states are reachable from this state.


// type sentence interface {
// 	Diamond(x int) bool
// 	Box(x int) bool
// 	Here(x int) bool
// 	Filter(xs []int) func(x int) bool
// 	Parse(sentence string) func(x int) bool
// 	Compose(preds []string) func(x int) bool
// }

// func (g gameboard) Compose(preds []string) func(x int) bool {
// 	return func(x int) bool {
// 		result := true
// 		for p := range preds {
// 			result = result && g.Parse(preds[p])(x)
// 		}
// 		return result
// 	}
// }

// func indexOf(arr []any, val any) int {
// 	for index, value := range arr {
// 		if value == val { return index }
// 	}
// 	return -1
// }

// func (g gameboard) Parse(sentence string) (func(x int) bool) {
// 	tokens := strings.Split(sentence, " ")
// 	if tokens[0] == "prop" {
// 		val := strconv.Atoi(tokens[1])
// 		return func(x int) bool {
// 			return x == val
// 		}
// 	}
// 	if tokens[0] == "and" {
// 		i := indexOf(tokens,"+'")
// 		return func(x int) bool {
// 			f1 := g.Parse(tokens[1:i])
// 			f2 := g.Parse(tokens[i:])
// 			return f1(x) && f2(x)
// 		}
// 	}
// 	if tokens[0] == "or" {
// 		i := indexOf(tokens,"+'")
// 		return func(x int) bool {
// 			f1 := g.Parse(tokens[:i])
// 			f2 := g.Parse(tokens[i:])
// 			return f1(x) || f2(x)
// 		}
// 	}
// 	if tokens[0] == "not" {
// 		return func(x int) bool {
// 			f1 := g.Parse(tokens[1])
// 			return !f1(x)
// 		}
// 	}
// 	if tokens[0] == "filter" {
// 		return g.Filter(token[1:])
// 	}
// 	if tokens[0] == "here" {
// 		return g.Here
// 	}
// 	if tokens[0] == "diamond" {
// 		return g.Diamond
// 	}
// 	if tokens[0] == "box" {
// 		return g.Box
// 	}
// 	return func(x int) bool { return false }
// }

// func (g gameboard) Filter(xs map[int]bool) func(int) bool {
// 	return func(x int) bool {
// 		_, hasKey := xs[x]
// 		return hasKey
// 	}
// }

// func (g gameboard) Here(x int) bool {
// 	return x == g.point
// }


// func (g gameboard) Diamond(x int) bool {

// 	if g.Here(x) { return true } // reflexivity lets us straightfowardly answer "is this reachable?" with Diamond
	
// 	var visited map[int]bool
// 	var itinerary []int
// 	itinerary = append(itinerary, g.point)
	
// 	for len(itinerary) > 0 {
// 		curr, itinerary := itinerary[0], itinerary[1:]
// 		for adj := range g.edges[curr] {
// 			if adj == x { return true }
// 			if !visited[adj] { itinerary = append(itinerary, adj) }
// 		}
// 	}
// 	return false
// }


// func (g gameboard) Box(x int) bool {


// 	for adj := range g.edges[g.point] {
// 		if adj != x { return false }
// 	}

// 	for adj := range g.edges[x] {
// 		if adj != x { return false }
// 	}

// 	return true
// }





// HOW DO PROPERTIES GET COMPARED??? Function equivalence is not actually solvable. Fuck. Um.
// okay so function equivalence is solved for enumerable functions
// and effectively finite modelable functions
// complexity of reachability as I constructe it??? who knows
// picture of board given the properties that I /do/ know??? who knows

// type Property interface {
// 	Predicate(x int) bool
// }



// type property struct {
// 	reachable RuneTrie
// 	unavoidable RuneTrie
// }



// func propertyCompose(p1, p2 property) property {
// 	var r property
// 	p1.reachable.Walk(r.Put)
// 	p2.reachable.Walk(r.Put)
// 	p1.unavoidable.Walk(r.Put)
// 	p2.unavoidable.Walk(r.Put)
	
// 	return r
// }

// func propertySubset(p1, p2 property) bool {

// 	f1 := func (key string, val interface {}) error {
// 		if !p1.reachable.Get(key) { return true }
// 	}
// 	if p2.reachable.Walk(f1) != nil { return false }

// 	f2 := func (key string, val interface {}) error {
// 		if !p1.reachable.Get(key) { return true }
// 	}
// 	if p2.unavoidable.Walk(f2) != nil { return false }

// 	return true
// }


type property struct {
	reachable, unavoidable [][]int
}

type Verifier interface {
	Check(model any) func (x any) bool
}


func (p property) Check(model gameboard) func (x int) bool {
	return func(x int) bool {
		reached := false
		avoided := true
		for nodeset := range reachable {
			reached = false
			for node := range nodeset {
				if model.point == node {
					reached = true
					break
				} // reflexivity lets us straightfowardly answer "is this reachable?" with Diamond
			}				

			var visited map[int]bool
			var itinerary []int
			itinerary = append(itinerary, model.point)
			
			for len(itinerary) > 0 {
				curr, itinerary := itinerary[0], itinerary[1:]
				for next := range model.edges[curr] {
					for node := range nodeset {
						if next == node {
							reached = true
							break
						}
					}
					if reached == true { break }
					if !visited[next] { itinerary = append(itinerary, next) }
				}
			}
		}

		for nodeset := range unavoidable {
			avoided = true
			for node := range nodeset {
				if model.point == node {
					avoided = false
					break
				} // reflexivity lets us straightfowardly answer "is this reachable?" with Diamond
			}			

			var visited map[int]bool
			var itinerary []int
			itinerary = append(itinerary, model.point)
			avoided := true
			
			for len(itinerary) > 0 {
				curr, itinerary := itinerary[0], itinerary[1:]
				for next := range model.edges[curr] {

					avoided = true
					for node := range nodeset {
						if next == node {
							avoided = false
							break
						}
					}
					if !visited[next] { itinerary = append(itinerary, next) }
				}
			}

		}
		
		return reached && !avoided
	}
}




type motivstate struct {
	g gameboard
	properties map[string]property 
}

// this is how we assign reachability semantics to the properties tracked by the motivstate
func (m motivstate) Predicate(x int)  bool {
	
	for n, p := m.properties {

	}
}


type Preference interface {
	Leq(x, y int) bool 	// this has to be implemented in a property-based player in a way that incorporates the motivstate-associated property predicate (and obey the axioms in doing so. how we manage that part is yet to be figured out.)
}

type player struct {
	ms map[motivstate]map[int][]int // I hate literally everything about this, chiefly that it has NO CONSTRAINTS when it comes to obeying the damn axioms relating motivstates to each other. Until we invent the beautiful data structure that lets us do that, here we fucking are. OUr preferences are associated with our motivestates and this lets us access themm when and where needed. constraints can come later.
	curr motivstate
}
type Motivstates interface {
	Update(preconditions) motivstate
}


func (p player) Leq(x,y int) bool {
	z := range p.ms[p.curr][x] {
		if z = y { return true } 
	}
	return false
}

// check that all mentioned prefs are about accessible states.
// TODO: does this automatically imply axiom 3? check.
func  IsReachable(p player) bool { // not checking for cycles. TODO: check for cycles here.
	for x, ys := range p.ms[p.curr] {
		if  !(p.curr.Predicate(x)) { return false }
		for y := range ys { if !(p.curr.Predicate(y)) { return false } }
	}
	return true
}

// function to identify the set of states that are indiostinguishable from state s according to player p
func partitionOf(p player, s state) bool {
	
}


func WinningStrategy(p player) {

}
