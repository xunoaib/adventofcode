import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import cache


def norm(s: str):
    return s.replace(' ', '')


lines = sys.stdin.read().splitlines()

values = {}
outputs = {}
inputs = defaultdict(list)

for line in lines:
    if m := re.match(r'^value (.*) goes to (.*)$', line):
        src, tar = map(norm, m.groups())
        values[int(src)] = tar
        src = int(src)
        inputs[tar].append(src)
        outputs[src] = tar
    elif m := re.match(r'^(.*) gives low to (.*) and high to (.*)$', line):
        src, low, high = map(norm, m.groups())
        outputs[src] = [low, high]
        inputs[low].append(src)
        inputs[high].append(src)

fixed = defaultdict(list)

while True:
    q = [
        (k, sorted(v)) for k, v in inputs.items()
        if len(v) > 1 and isinstance(v[0], int) and isinstance(v[1], int)
    ]

    if not q:
        break

    obj, vals = q.pop()
    del inputs[obj]

    for v, o in zip(vals, outputs[obj]):
        fixed[o].append(v)
        idx = inputs[o].index(obj)
        inputs[o][idx] = v

aa = next(k[3:] for k, v in fixed.items() if set(v) == {61, 17})
print('part1:', aa)
