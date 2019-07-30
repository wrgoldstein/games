import operator

class Route:
    all = []

    def __init__(self, from_city, to_city, length, color):
        self.from_city = from_city
        self.to_city = to_city
        self.length = int(length)
        self.color = color
        self.claimed = False
        Route.all.append(self)

    @staticmethod
    def from_cities(city1, city2):
        return filter(lambda r: r > [city1, city2], Route.all)
    
    @property
    def cities(self):
        return [self.from_city, self.to_city]

    def __gt__(self, cities):
        return set(self.cities) == set(cities)

    def __repr__(self):
        return "%s => %s, %s (%s)" % (self.from_city, self.to_city, self.length, self.color)
