#!/usr/bin/env python3
import math
import re
import sys


def findloops(dirs, net, node):
    step = 0
    seen = set()
    stepnode = {}
    while True:
        state = (node, step % len(dirs))
        if state in seen:
            return stepnode
        seen.add(state)
        stepnode[step] = node
        ndir = 'LR'.index(dirs[step % len(dirs)])
        node = net[node][ndir]
        step += 1


def findz(loops):
    return next((k for k, v in loops.items() if v[-1] == 'Z'))


def main():
    dirs, data = sys.stdin.read().strip().split('\n\n')
    lines = data.split('\n')

    net = {}
    for line in lines:
        src, left, right = re.search(r'(.*) = \((.*), (.*)\)', line).groups()
        net[src] = (left, right)

    ans1 = 0
    node = 'AAA'
    while node != 'ZZZ':
        i = 'LR'.index(dirs[ans1 % len(dirs)])
        node = net[node][i]
        ans1 += 1

    nodes = [n for n in net if n[-1] == 'A']
    zsteps = [findz(findloops(dirs, net, n)) for n in nodes]

    ans2 = gcd = math.gcd(zsteps[0], zsteps[1])
    for step in zsteps:
        ans2 *= step // gcd

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 18023
    assert ans2 == 14449445933179


if __name__ == '__main__':
    main()
