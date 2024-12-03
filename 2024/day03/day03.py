#!/usr/bin/env python3

import re
import sys

lines = sys.stdin.read().strip().splitlines()

p1 = 0
for line in lines:
    for a, b in re.findall(r'mul\((\d+),(\d+)\)', line):
        if len(a) < 4 and len(b) < 4:
            p1 += int(a) * int(b)

p2 = 0
enabled = True
for line in lines:
    for g in re.findall(r'(mul\(\d+,\d+\)|do\(\)|don\'t\(\))', line):
        if g == "don't()":
            enabled = False
        elif g == "do()":
            enabled = True
        elif enabled:
            a, b = re.findall(r'\d+', g)
            if len(a) < 4 and len(b) < 4:
                p2 += int(a) * int(b)

print('part1:', p1)
print('part2:', p2)
