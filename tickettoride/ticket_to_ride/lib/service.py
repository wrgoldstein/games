from player import Player

class Service:
    @staticmethod
    def deal_player_tickets(game, player, must_keep_two=False):
        tickets = game.ticket_deck.deal(3)
        to_keep = 2 if must_keep_two else 1
        kept, unkept = player.choose_tickets(tickets, to_keep)
        
        player.tickets += kept
        player.ticket_points -= sum([ticket.points for ticket in kept])

        game.ticket_deck.accept(unkept)

    @staticmethod
    def deal_player_trains(game, player, n):
        cards = game.train_deck.deal(n)
        player.trains += cards

    @staticmethod
    def check_if_its_over(game):
        if game.last_turns == len(game.players):
            game.winner = game.currently_winning()
            return True

    @staticmethod
    def check_if_its_almost_over(game, player):
        if game.last_turns is not None:
            game.last_turns += 1
        elif game.last_turns is None and player.train_count <= 3:
            game.last_turns = 0


    @staticmethod
    def take_action(game, action):
        player, t, args = action

        if t == 'Train':
            deck = args['Deck']
            # face_up = args['Face up'] #TODO
            Service.deal_player_trains(game, player, deck)

        elif t == 'Route':
            Service.claim_route(game, player, args['route'], args['color'])

        elif t == 'Ticket':
            Service.deal_player_tickets(game, player)

    @staticmethod
    def record_history(game, player, action):
        game.history.append([player, action])
            
        
    @staticmethod
    def claim_route(game, player, route, color):
		filtered = 0
		trains = []
		for train in player.trains:
			if train == color and route.length > filtered:
				filtered += 1
			else:
				trains.append(train)
		player.trains = trains
		player.train_count -= route.length
		game.train_deck.discards += list(route.length * color)
		route.claimed = True
		player.routes.append(route)
		player.satisfy_any_tickets()
		player.route_points += Player.ROUTE_SCORING[route.length]
		return