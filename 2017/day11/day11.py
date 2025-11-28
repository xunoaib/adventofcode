from collections import Counter

ds = input().split(',')

c = Counter(ds)

for a, b in [('ne', 'sw'), ('nw', 'se'), ('s', 'n')]:
    if c[b] < c[a]:
        a, b = b, a
    c[b] -= c[a]
    c[a] = 0

a, b = 'ne', 'nw'

if c[b] < c[a]:
    a, b = b, a

c['n'] += c[a]  # add nw + ne == n
c[b] -= c[a]
c[a] = 0

print('part1:', c['n'] + c['ne'])
