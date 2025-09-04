import sys
from itertools import cycle

ints = list(map(int, sys.stdin))

print('part1:', sum(ints))

freq = 0
seen = {freq}

for i in cycle(ints):
    freq += i
    if freq in seen:
        print('part2:', freq)
        break
    seen.add(freq)
