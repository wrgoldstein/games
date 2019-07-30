import uuid
from itertools import chain
from helpers import satisfied

class Player:
	_count = 0

	ROUTE_SCORING = {
	    1: 1,
	    2: 2,
	    3: 4,
	    4: 7,
	    5: 10,
	    6: 15
	}

	def __init__(self, strategy, kwargs):
		Player._count += 1
		self.name = "Player %s" % Player._count
		print('Welcome to the game,', self.name)
		self.strategy = strategy(self, **kwargs)
		self.refresh()

	def __repr__(self):
		return self.name + ", " + self.strategy.name

	def refresh(self):
		self.trains = []
		self.routes = []
		self.tickets = []
		self.ticket_points = 0
		self.route_points = 0
		self.train_count = 45

		self.history = {'score': [], 'max_values': []}

	def score(self):
		return self.route_points + self.ticket_points

	@property
	def points(self):
		return self.route_points, self.ticket_points

	def choose_tickets(self, tickets, to_keep):
		kept = tickets[:to_keep] #TODO defer to a strategy
		return kept, list(set(tickets).difference(kept))

	def action(self, game):
		return self.strategy.action(game)

	def trains_for_color(self, color):
		return [t for t in self.trains if t == color]

	def unsatisfied_tickets(self):
		return [ticket for ticket in self.tickets if not ticket.satisfied]

	def satisfied_tickets(self):
		return [ticket for ticket in self.tickets if ticket.satisfied]

	def satisfy_any_tickets(self):
		for ticket in self.unsatisfied_tickets():
			if satisfied(ticket, self.routes):
				ticket.satisfy()
				self.ticket_points += ticket.points

	def connected_cities(self):
		return list(chain(*map(lambda r: [r.from_city, r.to_city], self.routes)))
