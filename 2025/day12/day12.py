import re

r = open(0).read().strip().split('\n\n')[-1]
a1 = 0

for l in r.split('\n'):
    w, l, *c = map(int, re.findall(r'\d+', l))
    a1 += w * l >= sum(v * 9 for v in c)

print('part1:', a1)
