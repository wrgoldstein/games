from data import tickets
from copy import deepcopy
from random import shuffle

class TicketDeck(object):
    tickets = deepcopy(tickets)

    def __init__(self):
        self.tickets = deepcopy(TicketDeck.tickets)
    
    def deal(self, n):
        return [self.tickets.pop(0) for _ in range(n)]

    def accept(self, tickets):
    	self.tickets += tickets

    def shuffle(self):
        shuffle(self.tickets)