#!/usr/bin/env python3

import sys

s1, s2  = sys.stdin.read().strip().split('\n\n')

rules = [tuple(map(int, line.split('|'))) for line in s1.split('\n')]
updates = [tuple(map(int, line.split(','))) for line in s2.split('\n')]

def find_smallest(update):
    '''Find the only number which has no other numbers come before it'''

    right = [y for x,y in rules if x in update and y in update]

    for v in update:
        if v not in right:
            return v

def fix_order(update):
    fixed = []
    left = list(update)

    while left:
        s = find_smallest(left)
        fixed.append(s)
        left.remove(s)

    return fixed


def is_valid(update, x, y):
    if x in update and y in update:
        return update.index(x) < update.index(y)
    return True

p1 = p2 = 0

for update in updates:
    if all(is_valid(update, x,y) for x,y in rules):
        p1 += update[len(update)//2]
    else:
        update = fix_order(update)
        p2 += update[len(update)//2]

print('part1:', p1)
print('part2:', p2)
