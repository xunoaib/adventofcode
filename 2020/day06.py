#!/usr/bin/env python
import sys

groups = sys.stdin.read().strip().split('\n\n')
totany = 0
totall = 0

for group in groups:
    people = group.split('\n')

    # part 1
    chars = set(group.replace('\n',''))
    totany += len(chars)

    # part 2
    shared = set(people[0])
    for person in people[1:]:
        shared &= set(person)
    totall += len(shared)

print('part1:', totany)
print('part2:', totall)
