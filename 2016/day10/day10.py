import math
import re
import sys
from collections import defaultdict

outputs = {}
inputs = defaultdict(list)

for line in sys.stdin:
    if m := re.match(r'^value (.*) goes to (.*)$', line):
        src, tar = m.groups()
        src = int(src)
        outputs[src] = tar
        inputs[tar].append(src)
    elif m := re.match(r'^(.*) gives low to (.*) and high to (.*)$', line):
        src, low, high = m.groups()
        outputs[src] = [low, high]
        inputs[low].append(src)
        inputs[high].append(src)


def can_resolve(vals):
    return len(vals) == 2 and all(isinstance(v, int) for v in vals)


q = [(node, vals) for node, vals in inputs.items() if can_resolve(vals)]

while q:
    node, vals = q.pop()
    for val, out in zip(sorted(vals), outputs[node]):
        inputs[out][inputs[out].index(node)] = val
        if can_resolve(inputs[out]):
            q.append((out, inputs[out]))

a1 = next(int(k[4:]) for k, v in inputs.items() if set(v) == {61, 17})
print('part1:', a1)

a2 = math.prod(inputs[f'output {o}'][0] for o in range(3))
print('part2:', a2)

assert a1 == 118
assert a2 == 143153
