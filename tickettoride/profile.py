import cProfile
import pstats

from ticket_to_ride import TicketToRide, Player, DefaultStrategy, SimpleOptimizer

def run():
	gameboard = TicketToRide()
	Player(SimpleOptimizer).sit(gameboard)
	Player(DefaultStrategy).sit(gameboard)
	gameboard.setup()
	gameboard.simulate()

cProfile.run('run()', 'restats')
p = pstats.Stats('restats')

p.sort_stats('cumulative').print_stats(20)
