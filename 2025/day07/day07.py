import sys
from collections import Counter

lines = sys.stdin.read().strip().split('\n')
rows = [[i for i, v in enumerate(line) if v == '^'] for line in lines]

beams = Counter({lines[0].index('S'): 1})
a1 = 0

for splits in rows:
    curbeams = beams.copy()
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
