package main

import (
	"fmt"
	"io/ioutil"
	"math"
)

func main() {
	fmt.Println("Dietrich-List Reachability Game")
}


// We have to reimplement all the base machinery here, which means we can /improve/ it hopefully.
// How Posets? Seriously tho. (Probably a Hasse diagram as a map. Simplest way.)
// How do we check that a map is a legal Hasse diagram? (Well, we check for cycles, like the typical DP problem would have us do.)

// Game states are int, all states are "alternatives" i.e. can be preferred or dispreferred.

type gameboard struct {
	edges map[int][]int
	point int
}



// Under reachability, properties are just claims abot what states are reachable from this state.


type property interface {
	Diamond(x int) bool
	Box(x int) bool
	Here(x int) bool
}

func (g gameboard) Here(x int) bool {
	return x == g.point
}


func (g gameboard) Diamond(x int) bool {

	if g.Circle(x) { return true }
	
	visited = map[int]bool
	itinerary = []int
	itinerary.append(g.point)
	
	while len(itinerary) > 0 {
		curr, itinerary = itinerary[0], itinerary[1:]
		else {
			visited[curr] = true
			for adj := range g.edges[curr] {
				if adj == x { return true }
				else if !visited[adj] { itinerary.append(adj) } }
		}
	}
	return false
}


func (g gameboard) Box(x int) bool {


	for adj := range g.edges[g.point] {
		if adj != x { return false }
	}

	for adj := range g.edges[x] {
		if adj != x { return false }
	}

	return true
}



type motivstate struct {
	.
}
