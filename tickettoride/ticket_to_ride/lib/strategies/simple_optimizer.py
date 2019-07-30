from default_strategy import DefaultStrategy
from ..helpers import route_options, distance, satisfied, bfs_paths, RouteGraph, route_graph_from_routes

class SimpleOptimizer(DefaultStrategy):
	def action(self):
		"""
		Among possible routes to purchase, choose one that best
		connects two cities you have tickets for
		"""

		best_route = self.choose_best_route()
		if best_route is not None:
			color = self.route_solutions(best_route)[0]
			self.player.claim_route(best_route, color)
			return
		elif self.player.gameboard.train_deck.cards_left() >= 2:
			self.pick_best_train_cards()
		else:
			self.player.draw_ticket(1)
		pass

	def __str__(self):
		return "SimpleOptimizer"

	def choose_best_route(self):
		claimable = self.claimable_routes()
		if not claimable: return None
		scores = []
		for route in claimable:
			score = self.score_route(route)
			scores.append(score)
		
		best_route = sorted(claimable, key=lambda a: scores[claimable.index(a)])[-1]
		if max(scores) > 0:
			return best_route


	def score_route(self, route):
		"""
		Give a relative value to each route.

		is in a path for a ticket: +1 for each city in the path
		(only one path contributes, minimum +1)

		"""

		tickets = self.player.unsatisfied_tickets()
		score = 0

		unclaimed_routes = [route for route in self.player.gameboard.routes if not route.claimed and route not in self.player.routes]
		route_graph = route_graph_from_routes(unclaimed_routes)

		for ticket in tickets:
			ticket_distance = distance(ticket.from_city, ticket.to_city)

			#TODO routegraph should exclude routes claimed by others
			#TODO this `bfs_paths` usage could be more efficient if it reused an existing path list
			possible_paths = bfs_paths(route_graph, ticket.from_city, ticket.to_city, ticket_distance + 2)

			for path in possible_paths:
				if route.from_city in path or route.to_city in path:
					score = max(1, score)
				
				score = max(score, len(set(path).intersection(self.player.connected_cities())))
		
		return score


	#TODO whether to choose a route
	#TODO which route to choose
	#TODO whether to choose a ticket

		
			
			