import math
import re

O = {}
I = {}

for L in open(0):
    if m := re.match(r'^value (.*) goes to (.*)$', L):
        s, t = m.groups()
        O[int(s)] = t
        I[t] = I.get(t, []) + [int(s)]
    elif m := re.match(r'^(.*) gives low to (.*) and high to (.*)$', L):
        s, l, h = m.groups()
        O[s] = [l, h]
        I |= {k: I.get(k, []) + [s] for k in [l, h]}


def f(V):
    return len(V) == 2 and all(isinstance(v, int) for v in V)


q = [(n, v) for n, v in I.items() if f(v)]

while q:
    n, v = q.pop()
    for v, o in zip(sorted(v), O[n]):
        I[o][I[o].index(n)] = v
        q += [(o, I[o])] * f(I[o])

a = next(int(k[4:]) for k, v in I.items() if set(v) == {61, 17})
b = math.prod(I[f'output {o}'][0] for o in '012')

print(a)
print(b)

assert a == 118
assert b == 143153
