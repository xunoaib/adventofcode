from collections import Counter

ORDERS = 'n ne se s sw nw'.split() * 2


def measure_dist(ds):
    c = Counter(ds)

    for a, b in [('ne', 'sw'), ('nw', 'se'), ('s', 'n')]:
        if c[b] < c[a]:
            a, b = b, a
        c[b] -= c[a]
        c[a] = 0

    def combine(a, b, into):
        # cancels out moves (nw + ne become n)
        if c[b] < c[a]:
            a, b = b, a

        c[into] += c[a]
        c[b] -= c[a]
        c[a] = 0

    for i in range(6):
        a, into, b = ORDERS[i:i + 3]
        combine(a, b, into)

    return sum(c.values())


ds = input().split(',')

a1 = a2 = 0

for i in range(len(ds)):
    a1 = measure_dist(ds[:i + 1])
    a2 = max(a2, a1)

print('part1:', a1)
print('part2:', a2)

assert a1 == 764
assert a2 == 1532
