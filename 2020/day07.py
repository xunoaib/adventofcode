#!/usr/bin/env python
import sys
import parse
from collections import defaultdict

class Bag:
    def __init__(self, rule):
        self.color, contents = parse.parse('{} bags contain {}.', rule)
        self.num_bags = None  # total number of bags that can be stored

        if contents == 'no other bags':
            self.storage = []
        else:
            groups = contents.split(', ')
            parsed = [parse.parse('{} {} bag', bag.strip('s')) for bag in groups]
            self.storage = [(color, int(count)) for count, color in parsed]

    def can_store(self, color):
        for bcolor, bcount in self.storage:
            if color == bcolor:
                return True
        return False

    def count_bags(self, bag_rules):
        '''Counts the number of bags that can be stored and caches the result to avoid costly recursive recalculations'''
        if self.num_bags:
            return self.num_bags

        self.num_bags = 0
        for color, count in self.storage:
            self.num_bags += count + count * bag_rules[color].count_bags(bags)
        return self.num_bags

def count_bags_recursive(bags, color):
    # maps stored color to all possible parents
    parents_graph = defaultdict(set)
    for parent_color, bag in bags.items():
        for child_color, _ in bag.storage:
            parents_graph[child_color].add(parent_color)

    # explore and count all possible parents
    visited = set()
    frontier = [color]

    while frontier:
        color = frontier.pop()
        parents = parents_graph[color] - visited  # only enqueue unvisited parents
        frontier += parents
        visited |= parents
    return len(visited)

rules = sys.stdin.readlines()
bags = {bag.color: bag for bag in map(Bag, rules)}

numbags = count_bags_recursive(bags, 'shiny gold')
print('part1:', numbags)

numbags = bags['shiny gold'].count_bags(bags)
print('part2:', numbags) # bah numbag
