import sys
from collections import Counter

a1 = a2 = None

s = sys.stdin.read()
lines = s.strip().split('\n')

beams = {i for i, ch in enumerate(lines[0]) if ch == 'S'}
a1 = a2 = 0

for line in lines:
    for i, ch in enumerate(line):
        if ch == '^':
            if i in beams:
                beams.remove(i)
                beams |= {i - 1, i + 1}
                a1 += 1

beams = Counter(i for i, ch in enumerate(lines[0]) if ch == 'S')

for line in lines:
    newbeams = beams.copy()
    for i, ch in enumerate(line):
        if ch == '^':
            if count := beams.get(i):
                newbeams[i] -= count
                newbeams[i - 1] += count
                newbeams[i + 1] += count
                a2 += count
    beams = newbeams

print('part1:', a1)
print('part2:', a2)

assert a1 == 1541
assert a2 == 80158285728929
