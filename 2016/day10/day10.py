import math
import re
import sys
from collections import defaultdict

lines = sys.stdin.read().splitlines()
outputs = {}
inputs = defaultdict(list)

for line in lines:
    if m := re.match(r'^value (.*) goes to (.*)$', line):
        src, tar = m.groups()
        src = int(src)
        inputs[tar].append(src)
        outputs[src] = tar
    elif m := re.match(r'^(.*) gives low to (.*) and high to (.*)$', line):
        src, low, high = m.groups()
        outputs[src] = [low, high]
        inputs[low].append(src)
        inputs[high].append(src)

fixed = defaultdict(list)

while True:
    q = [
        (o, sorted(v)) for o, v in inputs.items()
        if len(v) > 1 and isinstance(v[0], int) and isinstance(v[1], int)
    ]

    if not q:
        break

    obj, vals = q.pop()
    del inputs[obj]

    for v, o in zip(vals, outputs[obj]):
        fixed[o].append(v)
        inputs[o][inputs[o].index(obj)] = v

a1 = next(int(k[4:]) for k, v in fixed.items() if set(v) == {61, 17})
print('part1:', a1)

a2 = math.prod(fixed[f'output {o}'][0] for o in [0, 1, 2])
print('part2:', a2)

assert a1 == 118
assert a2 == 143153
