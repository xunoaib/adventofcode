import sys
from itertools import cycle

ints = list(map(int, sys.stdin))

part1 = sum(ints)

freq = part2 = 0
seen = {freq}

for i in cycle(ints):
    freq += i
    if freq in seen:
        part2 = freq
        break
    seen.add(freq)

assert part1 == 406
assert part2 == 312

print('part1:', part1)
print('part2:', part2)
