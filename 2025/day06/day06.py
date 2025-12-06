import re
import sys

s = sys.stdin.read()
lines = s.strip().split('\n')


def part1():
    aa = 0
    for *vs, o in zip(*nums, ops):
        aa += eval(o.join(vs))
    return aa


maxlen = max(len(line) for line in lines)
*nums, ops = [re.split(r'\s+', line.strip()) for line in lines]

a1 = part1()

a2 = 0
buf = []

for c in range(0, maxlen):
    s = ''.join(lines[r][c] for r in range(len(nums))).strip()
    if s:
        buf.append(s)
    else:
        a2 += eval(ops.pop(0).join(buf))
        buf.clear()

if ops:
    a2 += eval(ops.pop(0).join(buf))

print('part1:', a1)
print('part2:', a2)

assert a1 == 4309240495780
assert a2 == 9170286552289
