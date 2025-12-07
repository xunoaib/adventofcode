import sys
from collections import Counter

lines = sys.stdin.read().strip().split('\n')
start = lines[0].index('S')
lines = [[i for i, v in enumerate(line) if v == '^'] for line in lines]

beams = Counter({start: 1})
a1, a2 = 0, 1

for splits in lines:
    newbeams = beams.copy()
    for i in splits:
        if count := beams.get(i):
            newbeams[i] -= count
            newbeams[i - 1] += count
            newbeams[i + 1] += count
            a2 += count
            a1 += 1
    beams = newbeams

print('part1:', a1)
print('part2:', a2)

assert a1 == 1541
assert a2 == 80158285728929
