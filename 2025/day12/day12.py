import sys

*s, r = sys.stdin.read().strip().split('\n\n')
shapes = [g.count('#') for g in s]

a1 = 0
for line in r.split('\n'):
    a, *counts = line.split()
    w, l = map(int, a[:-1].split('x'))
    counts = map(int, counts)
    a1 += w * l >= sum(count * shape for count, shape in zip(counts, shapes))

print('part1:', a1)
