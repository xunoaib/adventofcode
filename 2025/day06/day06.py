import re
import sys

lines = sys.stdin.read().replace('\n', ' \n').rstrip().split('\n')
*nums, ops = [re.split(r'\s+', line.strip()) for line in lines]

a1 = sum(eval(o.join(vs)) for *vs, o in zip(*nums, ops))
a2 = 0
buf = []

for c in range(len(lines[0])):
    if s := ''.join(lines[r][c] for r in range(len(nums))).strip():
        buf.append(s)
    else:
        a2 += eval(ops.pop(0).join(buf))
        buf = []

print('part1:', a1)
print('part2:', a2)

assert a1 == 4309240495780
assert a2 == 9170286552289
