from ticket_to_ride import TicketToRide, Player, DefaultStrategy, SimpleOptimizer

def test_simple_optimizer():
	gameboard = TicketToRide()
	Player(SimpleOptimizer).sit(gameboard)
	Player(DefaultStrategy).sit(gameboard)
	gameboard.setup()
	gameboard.simulate()
	for player in gameboard.players:
		print(player.strategy, player.score())

	assert gameboard.winner is not None
	assert gameboard.winner in gameboard.players
