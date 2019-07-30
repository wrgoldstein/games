## What is this?

This repo contains code that allows for simulated games of [Ticket To Ride](http://www.daysofwonder.com/tickettoride/en/usa/).  The idea is that once the game is fully represented one can try different behaviors to try to find optimal strategies.  The goal is for me to win on monday night game nights.

## Specifications

game object
 - has a train card deck
 - has a ticket deck
 - has a game board (routes)
 - has a score keeping unit
 - has players
 - allow a player to take a turn
 - can kick off a game (consisting of all legal turns)
 - can report the score at any point
 
a train card deck can
 - be picked from to add to player train cards
 - accept discarded cards into a separate pile
 - reshuffles discard pile into a new deck when empty

a ticket deck can
 - be plucked from in sets of three and chosen among
 - returns not chosen cards to the bottom

each player
 - has points
 - has train cards
 - has tickets
 - has a decision unit
 - has the ability to take actions
 - can claim a route iff they can afford it
 
decision units
 - have a strategy
 - can calculate desirability of different plays according to their strategy
 - choose among available actions according to their desirability (and some chance)

actions
 - affect player score and train cards

## Strategy

The strategy as far as I can tell is to balance the point requirements of the following:
 - long routes which require more cards
 - connecting ticketed cities efficiently
 - collecting tickets
 - collecting resources/train cards