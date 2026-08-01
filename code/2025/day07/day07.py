import sys
from collections import Counter

beams = Counter({input().index('S'): 1})
a1 = 0

for line in sys.stdin:
    curbeams = beams.copy()
    splits = [i for i, v in enumerate(line) if v == '^']
    for i in splits:
        count = curbeams.get(i, 0)
        beams[i] -= count
        beams[i - 1] += count
        beams[i + 1] += count
        a1 += count > 0

a2 = sum(beams.values())

print('part1:', a1)
print('part2:', a2)

assert a1 == 1541
assert a2 == 80158285728929
