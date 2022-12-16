#!/usr/bin/env python3
import re
import sys
from collections import defaultdict
from itertools import pairwise
from heapq import heappush, heappop

def find_all_shortest_paths(graph, start):
    """Finds the shortest travel costs between all nodes"""
    q = [(0, start)]
    visited = set()
    costs = {}
    while q:
        cost, node = heappop(q)
        visited.add(node)
        if cost < costs.get(node, sys.maxsize):
            costs[node] = cost

        for next_node in graph[node][1]:
            if next_node not in visited:
                heappush(q, (cost + 1, next_node))

    del costs[start]
    return costs


def find_flowing_costs(graph):
    """ Returns the shortest total travel cost between nodes with non-zero flow """
    flowing_nodes = [valve for valve, (rate, valves) in graph.items() if rate]
    route_costs = defaultdict(list)

    for node in flowing_nodes:
        node_paths = find_all_shortest_paths(graph, node)
        for tar, cost in node_paths.items():
            if tar in flowing_nodes:
                route_costs[node].append((tar, cost))
    return dict(route_costs)

rates = {}

MAX_MINUTE = 30

def calculate_pressure(valves, max_minute=MAX_MINUTE):
    pressure = sum((max_minute - minute) * rates[node] for node, minute in valves.items())
    return pressure

def solve(costs, node, minute, valves):
    valves = valves.copy()
    if minute <= MAX_MINUTE:
        valves[node] = minute

    if len(valves) == len(costs) or minute > MAX_MINUTE:
        return calculate_pressure(valves), valves

    results = []
    for next_node, cost in costs[node]:
        if next_node not in valves:
            result = solve(costs, next_node, minute + cost + 1, valves)
            results.append(result)

    results += [(calculate_pressure(valves), valves)]
    return max(results, key=lambda v: v[0])


def get_travel_cost(travel_costs, src, tar):
    for node, cost in travel_costs[src]:
        if node == tar:
            return cost


def calc_times(nodes, flow_travel_costs, start_travel_costs):
    curtime = start_travel_costs[nodes[0]] + 1
    times = {nodes[0]: curtime}
    for n1, n2 in pairwise(nodes):
        cost = get_travel_cost(flow_travel_costs, n1, n2)
        curtime += cost + 1
        times[n2] = curtime
    return times

def main():
    lines = sys.stdin.read().strip().split('\n')
    graph = {}

    for line in lines:
        m = re.match(r'Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)', line)
        valve, rate, valves = m.groups()
        graph[valve] = (int(rate), valves.split(', '))
        rates[valve] = int(rate)

    start_node = 'AA'
    start_travel_costs = find_all_shortest_paths(graph, start_node)
    flow_travel_costs = find_flowing_costs(graph)

    # find a path to each flowing target and then try to solve from there
    results = []
    for tar in flow_travel_costs:
        minute = start_travel_costs[tar]
        result = solve(flow_travel_costs, tar, minute + 1, {})
        results.append(result)
    cost, valves = max(results)
    print('part1:', cost)

if __name__ == '__main__':
    main()
