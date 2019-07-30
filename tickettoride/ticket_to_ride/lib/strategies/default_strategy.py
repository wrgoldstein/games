from collections import Counter
import random

class DefaultStrategy:
	"""
	The default strategy will be to claim a random available route if possible
	and otherwise draw from the deck.
	"""

	def __init__(self, player, **kwargs):
		self.player = player
		self.name = "default"

	def action(self, game):
		"""
		Take a random route if possible, otherwise take
		the top two train cards.
		"""
		claimable = self.claimable_routes(game)

		if len(claimable):
			route = claimable[0]
			color = self.route_solutions(route)[0]
			return (self.player, 'Route', {"route": route, "color": color})
		elif game.train_deck.cards_left() >= 2:
			return (self.player, 'Train', {'Deck': 2})
		else:
			return (self.player, 'Ticket', { "Number": 1 })
	

	def pick_best_train_cards(self):
		"""
		Pick two cards off the top of the deck.
		"""

		return (self.player, 'Train', {"Deck": 2, "Face up": 0})

	def claimable_routes(self, game):
		claimable = []
		claimed_pairs = [r.cities for r in self.player.routes]
		for route in game.routes:
			if not route.claimed and self.route_solutions(route):
				# A double route cannot be claimed twice
				if (route.from_city, route.to_city) not in claimed_pairs:
					claimable.append(route)
		return claimable

	def route_solutions(self, route):
		"""
		Given a player's available train cards, what can they use to 
		claim a given route.
		"""
		solutions = []
		for color in 'bgkoprwy':
			if route.color == color or route.color == '-':
				if len(self.player.trains_for_color(color)) >= route.length: 
					solutions.append(color)
		return solutions

	def route_solution_distance(self, route):
		"""
		You could add complexity here; sometimes for strategic reasons
		we would prefer one color to another if we could solve a route
		both ways. We'll ignore that for now.
		"""
		need = route.length
		for color in 'bgkoprwy':
			if route.color == color or route.color == '-':
				have = len(self.player.trains_for_color(color))
				if have >= route.length: 
					return 0
				else:
					if route.length - have < need:
						need = route.length - have
		return need