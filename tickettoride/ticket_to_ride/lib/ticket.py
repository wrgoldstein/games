class Ticket:
    all = []

    def __init__(self, from_city, to_city, points):
        self.from_city = from_city
        self.to_city = to_city
        self.points = int(points)
        self.satisfied = False
        Ticket.all.append(self)

    def __repr__(self):
        satisfaction = "(not satisfied)" if not self.satisfied else ""
        return """
        Ticket {satisfaction}
        from: {from_city}
        to:   {to_city}
        points: {points}
        """.format(
            satisfaction=satisfaction,
            from_city=self.from_city,
            to_city=self.to_city,
            points=self.points
        )

    @staticmethod
    def from_cities(city1, city2):
        return filter(lambda t: set(t.cities) == set([city1, city2]), Ticket.all)[0]

    @property
    def cities(self):
        return self.from_city, self.to_city

    def satisfy(self):
        self.satisfied = True