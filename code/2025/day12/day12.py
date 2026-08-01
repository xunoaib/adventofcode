import re

s = open(0).read().strip().split('\n\n')[-1]
a1 = 0

for l in s.split('\n'):
    w, l, *c = map(int, re.findall(r'\d+', l))
    a1 += w * l >= sum(c) * 9

print('part1:', a1)
