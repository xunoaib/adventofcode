import sys
from itertools import product


def neighbors8(r, c):
    for roff, coff in product([-1, 0, 1], repeat=2):
        if roff or coff:
            yield r + roff, c + coff


def accessible(g):
    for p in g:
        if sum(1 for n in neighbors8(*p) if n in g) < 4:
            yield p


papers = {
    (r, c)
    for r, line in enumerate(sys.stdin)
    for c, ch in enumerate(line) if ch == '@'
}

a1 = len(list(accessible(papers)))
a2 = 0

while acc := set(accessible(papers)):
    a2 += len(acc)
    papers -= acc

print('part1:', a1)
print('part2:', a2)

assert a1 == 1523
assert a2 == 9290
