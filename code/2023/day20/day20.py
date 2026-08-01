#!/usr/bin/env python3
import sys
from collections import Counter

HIGH, LOW = True, False


class Node:

    def __init__(self, name):
        self.name = name
        self.outputs = []
        self.inputs = []
        self.memory = []  # of previous input values (conjunctions only)
        self.on = False  # (flip-flops only)

    def reset(self):
        self.on = False
        self.memory = [LOW] * len(self.inputs)

    def add_output(self, *nodes):
        self.outputs += nodes

    def add_input(self, *nodes):
        self.inputs += nodes
        self.memory += [LOW] * len(nodes)

    def send(self, inpulse, innode=None):
        return self.prep_outputs(LOW)

    def prep_outputs(self, outpulse):
        return [(self, n, outpulse) for n in self.outputs]

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    def __hash__(self):
        return hash(self.name)


class FlipFlop(Node):

    def send(self, inpulse, innode=None):
        if inpulse == HIGH:
            return []
        self.on = not self.on
        return self.prep_outputs(self.on)


class Conjunction(Node):

    def send(self, inpulse, innode):
        idx = self.inputs.index(innode)
        self.memory[idx] = inpulse
        return self.prep_outputs(LOW in self.memory)


class Simulation:

    def __init__(self, nodes):
        self.nodes = nodes

    def reset(self):
        for n in self.nodes.values():
            n.reset()

    def push_button(self):
        q = self.nodes['broadcaster'].send(LOW)
        counts = Counter({LOW: 1})
        events = []
        while q:
            src, dst, signal = q.pop(0)
            counts[signal] += 1
            events.append((src, dst, signal))
            q += dst.send(signal, src)
        return counts, events


def find_common_exit(node):
    '''Finds the next node which is common to ALL paths starting from a given node'''

    paths = []
    visited = {node}
    q = [(node, )]
    while q:
        path = q.pop()
        if outputs := path[-1].outputs:
            for neighbor in outputs:
                if neighbor not in visited:
                    q.append(path + (neighbor, ))
                    visited.add(neighbor)
        else:
            paths.append(path)

    common = list(paths[0])
    for s in paths[1:]:
        common = [n for n in common if n in s]

    return common[1]


def main():
    lines = sys.stdin.read().strip().split('\n')
    nodes = {}

    for line in lines:
        name = line.split(' ')[0].lstrip('%&')
        cls = {'%': FlipFlop, '&': Conjunction}.get(line[0], Node)
        nodes[name] = cls(name)

    for line in lines:
        name = line.split(' ')[0].lstrip('%&')
        node = nodes[name]
        outputs = line.split(' ', 2)[-1].split(', ')
        for n in outputs:
            if n not in nodes:
                nodes[n] = Node(n)
            node.add_output(nodes[n])
            nodes[n].add_input(node)

    s = Simulation(nodes)
    counts = Counter()
    for _ in range(1000):
        counts += s.push_button()[0]
    a1 = counts[LOW] * counts[HIGH]

    print('part1:', a1)

    # Part 2: Identify the repeating interval for each cluster by independently
    # running the simulation until their first "exit" node outputs a LOW
    # signal. Then, LCM of these finds the interval when all will
    # simultaneously output LOW.

    a2 = 1
    b = nodes['broadcaster']
    for start in list(b.outputs):
        s.reset()
        end = find_common_exit(start)
        b.outputs = [start]
        presses = 0
        while True:
            _, events = s.push_button()
            presses += 1
            if any(src == end and signal == LOW for src, _, signal in events):
                break
        a2 *= presses

    print('part2:', a2)

    assert a1 == 711650489
    assert a2 == 219388737656593


if __name__ == '__main__':
    main()
