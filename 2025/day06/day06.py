import re
import sys

s = sys.stdin.read()
lines = s.strip().split('\n')


def part1():
    aa = 0
    for a, b, c, d, o in zip(*nums, ops):
        aa += eval(f'{a}{o}{b}{o}{c}{o}{d}')
    return aa


maxlen = max(len(line) for line in lines)
*nums, ops = [re.split(r'\s+', line.strip()) for line in lines]

a1 = part1()
a2 = 0

outs = []
for c in range(0, maxlen):
    s = ''
    for r, row in enumerate(nums):
        s += lines[r][c]
    s = s.strip()
    outs.append(s)

if outs[-1] != '':
    outs.append('')

buf = []
a2 = opidx = 0

while outs:
    if v := outs.pop(0):
        buf.append(v)
    else:
        a2 += eval(ops[opidx].join(buf))
        opidx += 1
        buf.clear()

print('part1:', a1)
print('part2:', a2)

assert a1 == 4309240495780
assert a2 == 9170286552289
