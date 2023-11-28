#!/usr/bin/env python3

part1 = len([x for x in open('day04.in') if len(set(x.split())) == len(x.split())])
part2 = len([x for x in open('day04.in') if len(x.split()) == len(set(tuple(y) for y in map(sorted, x.split())))])

print(part1)
print(part2)
