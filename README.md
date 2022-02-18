# Preference Sandbox

Sandbox for playing with preference structures.


## Dietrich & List - Where do Preferences Come From?


`dl-toy.py` and `dl-toy-2.py` are both terrible first drafts of the system described in this paper.

Type system in the comments of `dl-toy-2.py` suggests a better structure for it going forward, utils that will be generally useful (particularly, orderings); as well that this all should probably be happening in Haskell. Translation pending my finding the will to go on.

## Fix Motivational States, Generalize Preferences

- Given a set of possible motivational states for a player, what constraints are applicable to player preferences?
- Wishlist: Given a relationship of motivational states to extensional gameplay, what constraints are applicable to player preferences?



## SWFs and Arrow's Impossibility Theorem (wishlist)

Implementing Bergson-Samuelson SWFs and a "proof" of Arrow's (algorithm for finding the dictator, satisfaction that it will always find one) would probably generate all the utilities I need, and the doubts / questions I have to boot.

Like: where are the gaps in SWFs where we can derive a nearby model that lets us _almost_ do the thing we want to do?

Or: how do we go from choice function to a mechanism that implements it?

Arrow's asks a question of the shape "does choice function have these nice proeprties?", and the machinery works to ask more "applied" questions. (Compare auction theory.)


