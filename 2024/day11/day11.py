#!/usr/bin/env python3


import sys

stones = tuple(map(int, input().split()))

for i in range(25):
    new = []
    for s in stones:
        if s == 0:
            new.append(1)
        elif len(str(s)) % 2 == 0:
            t = str(s)
            new += [int(t[:len(t)//2]), int(t[len(t)//2:])]
        else:
            new.append(s * 2024)
    stones = new

x = len(stones)
print('part1:', x)

# print('part1:', a1)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
