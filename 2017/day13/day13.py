import sys

lines = sys.stdin.read().strip().split('\n')

ranges: dict[int, int] = dict(tuple(map(int, l.split(': '))) for l in lines)

a1 = 0

for d in range(max(ranges) + 1):
    if r := ranges.get(d):
        pos = d % (2 * r - 2)
        if pos == 0:
            a1 += d * r

print('part1:', a1)

assert a1 == 1728
