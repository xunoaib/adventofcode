from collections import Counter

ORDERS = 'n ne se s sw nw'.split() * 2


def measure_dist(ds):
    c = Counter(ds)

    def combine(a, b, into):
        if c[b] < c[a]:
            a, b = b, a

        c[into] += c[a]
        c[b] -= c[a]
        c[a] = 0

    # cancel out opposite moves (i.e. n & s)
    for i in range(3):
        a, into, b = ORDERS[i], None, ORDERS[i + 3]
        combine(a, b, into)

    # simplify other moves (i.e. nw & ne == n)
    for i in range(6):
        a, into, b = ORDERS[i:i + 3]
        combine(a, b, into)

    del c[None]

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
