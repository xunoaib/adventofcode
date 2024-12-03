#!/usr/bin/env python3

import re
import sys

data = sys.stdin.read()

p1 = p2 = 0

for a, b in re.findall(r'mul\((\d+),(\d+)\)', data):
    if len(a) < 4 and len(b) < 4:
        p1 += int(a) * int(b)

print('part1:', p1)

enabled = True
for g in re.findall(r'(mul\(\d+,\d+\)|do\(\)|don\'t\(\))', data):
    if g == "don't()":
        enabled = False
    elif g == "do()":
        enabled = True
    elif enabled:
        a, b = re.findall(r'\d+', g)
        if len(a) < 4 and len(b) < 4:
            p2 += int(a) * int(b)

print('part2:', p2)
