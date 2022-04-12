package main

import (
	"fmt"
	"io/ioutil"
	"math"
)

fun main() {
	fmt.Println("Dietrich-List Reachability Game")
}


// We have to reimplement all the base machinery here, which means we can /improve/ it hopefully.
// How Posets? Seriously tho. (Probably a Hasse diagram as a map. Simplest way.)
// How do we check that a map is a legal Hasse diagram? (Well, we check for cycles, like the typical DP problem would have us do.)

type gameboard struct {
	edges map[int]int
}

