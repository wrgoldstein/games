import random
import numpy as np
from itertools import chain, izip_longest

from data import Route, routes, Ticket, tickets, cities

def shuffled(L):
    return sorted(L, key=lambda *args: random.random())

def defaultmax(L):
    if len(L):
        return max(L)
    return 0

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return filter(lambda a: None not in a, izip_longest(fillvalue=fillvalue, *args))


RouteGraph = dict()
for city in cities:
    RouteGraph[city] = set()
    for route in routes:
        if route.from_city == city:
            RouteGraph[city].add(route.to_city)
        elif route.to_city == city:
            RouteGraph[city].add(route.from_city)

def bfs(graph, start, subset=None):
    visited, queue = set(), [start]
    prev = {start: []}
    distances = {}
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            neighbors = graph[vertex] - visited
            queue.extend(neighbors)
            for neighbor in neighbors:
                if len(prev[vertex]) + 1 < distances.get(neighbor, np.inf):
                    prev[neighbor] = prev[vertex] + [vertex]
                    distances[neighbor] = len(prev[vertex]) + 1
    return distances

def bfs_paths(graph, start, goal, max_length=6):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            elif len(path) < max_length:
                queue.append((next, path + [next]))

distances = dict([(city, bfs(RouteGraph, city)) for city in cities])

def distance(from_city, to_city):
    return distances[from_city][to_city]
        
def route_options(from_city, to_city, max_length):
    return list(bfs_paths(RouteGraph, from_city, to_city, max_length))

def satisfied(ticket, routes, verbose=False):
    route_graph = route_graph_from_routes(routes)
    connected = bfs(route_graph, ticket.from_city)
    return ticket.to_city in connected

def route_graph_from_routes(routes):
    graph = dict()
    for city in cities:
        graph[city] = set()
        for route in routes:
            if route.from_city == city:
                graph[city].add(route.to_city)
            elif route.to_city == city:
                graph[city].add(route.from_city)
    return graph
