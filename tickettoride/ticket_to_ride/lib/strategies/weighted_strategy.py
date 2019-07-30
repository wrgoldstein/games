# -*- coding: utf-8 -*-

import operator
from collections import defaultdict
from itertools import chain, permutations, izip_longest

from default_strategy import DefaultStrategy
from ..helpers import route_options, distance, satisfied, bfs_paths, RouteGraph, route_graph_from_routes, grouper
from ..route import Route

###
import pdb
###

class WeightedStrategy(DefaultStrategy):
    def __init__(self, player, **kwargs):
        
        self.player = player

        self.alpha = kwargs.get("alpha",  1000)     # how much do we want to take the shortest route (inverse δ above)
        self.beta = kwargs.get("beta",  1)       # how impatient are we? how much of a premium do we put on taking available routes
        self.gamma = kwargs.get("gamma",  50)     # how much do we reward building on existing routes
        # delta is how "mean" we are-- how much do we try to block
        self.epsilon = kwargs.get("epsilon",  .5) # how much do we like long roads?
        self.M = kwargs.get("M", 50)             # how much must a route be worth before it's worth claiming
        self.m = kwargs.get("m", 0)              # how much does M change over time

        self.history = defaultdict(list)
        self.name = u"weighted: alpha: {alpha} beta: {beta} gamma: {gamma} epsilon: {epsilon}".format(
            alpha=self.alpha, beta=self.beta, gamma=self.gamma, epsilon=self.epsilon
        )

    def action(self, game):
        claimable = self.claimable_routes(game)
        scored = self.score_routes(game)
        
        if len(scored):
            self.player.history['max_values'].append(max([v for _,v in scored])) 

        self.M += self.m
        for route, value in scored:
            if route in claimable and value >= self.M:
                color = self.route_solutions(route)[0]
                return (self.player, 'Route', {"route": route, "color": color})

        if game.train_deck.cards_left() >= 2:
            return self.pick_best_train_cards()
        else:
            return (self.player, 'Ticket', { "Number": 1 }) # number not used yet

    def __repr__(self):
        return "Weighted"

    def feasible_paths(self, game, ticket):
        m = distance(ticket.from_city, ticket.to_city)
        padding = 2
        """
        we will not want to recalculate this graph and paths all the time!

        but for now its ok
        """

        graph = route_graph_from_routes(game.unclaimed_routes() + self.player.routes)
        paths = bfs_paths(graph, ticket.from_city, ticket.to_city, m + padding)
        return list(paths)

    def score_routes(self, game):
        """
        We will eventually look to store route scores and not recalculate them
        each time.... but for now we want to prove this approach works at all..
        """

        route_scores = defaultdict(int)

        alpha = 0
        beta = 0
        gamma = 0
        epsilon = 0
        
        paths = []
        for ticket in self.player.tickets:
            paths += self.feasible_paths(game, ticket)

        min_length = min(map(len, paths)) if len(paths) else 1000
        for path in paths:
            score = 0
            edges = list(grouper(2, path))

            if None in edges[-1]:
                edges.pop()
            
            # BONUS FOR BEING A SHORT PATH THAT SOLVES A TICKET 

            if len(path) == min_length:
                score += self.alpha * (0.5**(len(path) - min_length))
                alpha += self.alpha * (0.5**(len(path) - min_length))
                
            for edge in edges:

                routes = game.routes_from_cities(*edge)

                # HOW CLOSE TO FINISHING
                score += self.beta * max(0, 6 - min(map(self.route_solution_distance, routes)))
                beta += self.beta * max(0, 6 - min(map(self.route_solution_distance, routes)))

                if any([c > routes[0].cities for c in self.player.routes]):
                    # slightly complicated because a city pairing can appear twice
                    # which is a quirk that makes the double routes easier to manage
                    score += self.gamma
                    gamma += self.gamma

                # ROUTE LENGTH
                score += self.epsilon * self.player.ROUTE_SCORING[routes[0].length]
                epsilon += self.epsilon * self.player.ROUTE_SCORING[routes[0].length]

                    
            # we do this twice since we want to reward all
            # routes for being in paths with other claimed
            # routes

            for edge in edges:
                routes = game.routes_from_cities(*edge)
                for route in routes:
                    route_scores[route] += score

        self.history['alpha'].append(alpha)
        self.history['beta'].append(beta)
        self.history['gamma'].append(gamma)
        self.history['epsilon'].append(epsilon)

        sorted_routes = sorted(route_scores.items(), key=operator.itemgetter(1))
        return list(reversed(sorted_routes))
