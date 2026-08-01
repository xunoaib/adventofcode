#!/usr/bin/env python3
import sys

def part1(crabs):
    costs = set()
    for i in range(min(crabs), max(crabs)+1):
        costs.add(sum(abs(crab - i) for crab in crabs))
    return min(costs)

def consecutive_sum(n):
    return (n * (n+1)) // 2

def part2(crabs):
    costs = set()
    for i in range(min(crabs), max(crabs)+1):
        costs.add(sum(consecutive_sum(abs(crab - i)) for crab in crabs))
    return min(costs)

def main():
    crabs = list(map(int, sys.stdin.read().split(',')))

    ans1 = part1(crabs)
    print('part1:', ans1)

    ans2 = part2(crabs)
    print('part2:', ans2)

    assert ans1 == 344138
    assert ans2 == 94862124

if __name__ == '__main__':
    main()
