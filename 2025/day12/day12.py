import sys

*gs, end = sys.stdin.read().strip().split('\n\n')
shapes = []

for g in gs:
    lines = g.split('\n')[1:]
    shapes.append(
        {
            (r, c)
            for r, line in enumerate(lines)
            for c, ch in enumerate(line) if ch == '#'
        }
    )

a1 = 0
for line in end.split('\n'):
    a, *counts = line.split()
    w, l = map(int, a[:-1].split('x'))
    counts = map(int, counts)
    size = sum(count * len(shape) for count, shape in zip(counts, shapes))
    a1 += size <= w * l

print('part1:', a1)
