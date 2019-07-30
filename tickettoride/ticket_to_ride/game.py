from copy import deepcopy
from collections import defaultdict

from lib.data import cities, Route, routes, Ticket, tickets
from lib.train_deck import TrainDeck
from lib.ticket_deck import TicketDeck
from lib.player import Player
from lib.strategies import DefaultStrategy, SimpleOptimizer, WeightedStrategy
from lib.service import Service
from lib import helpers


class Game:
    
    def __init__(self, *players):
        self.players = players
        self.routes = deepcopy(routes)
        self.winner = None
        self.train_deck = TrainDeck()
        self.ticket_deck = TicketDeck()
        self.face_up = []
        self.longest_path_bonus = None
        self.last_turns = None
        self.n_turns = 0
        self.scores = defaultdict(list)
        self.actions = defaultdict(list)

    def pick_who_goes_first(self):
        self.players = helpers.shuffled(self.players)

    def routes_from_cities(self, city1, city2):
        return filter(lambda r: set(r.cities) == set([city1, city2]), self.routes)

    def setup(self):
        self.train_deck.shuffle()
        self.ticket_deck.shuffle()

        for player in self.players:
            player.refresh()
            Service.deal_player_trains(self, player, 4)
            Service.deal_player_tickets(self, player, True)

        #TODO
        # self.face_up = self.train_deck.deal(5)

        #TODO  # Longest Path Bonus isn't set
            

    def game_turn(self):
        # perform a single turn of the game
        for player in self.players:
            if Service.check_if_its_over(self): return
            action = player.action(self)
            Service.take_action(self, action)
            Service.check_if_its_almost_over(self, player)

            # record keeping
            self.actions[player.name].append(action[1])
            self.scores[player.name].append(player.score())



    def play(self):
        self.pick_who_goes_first()
        self.setup()

        while self.winner is None:
            self.game_turn()
            self.n_turns += 1

            if self.n_turns > 100:
                print "DID NOT FINISH"
                break
        
    
    def currently_winning(self):
        i = max(range(len(self.players)), key=lambda x: self.players[x].score())
        return self.players[i]

    def unclaimed_routes(self):
        return filter(lambda r: not r.claimed,  self.routes)
