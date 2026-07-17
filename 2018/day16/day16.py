import re
import sys
from collections import defaultdict

OPNAMES = (
    'addi',
    'addr',
    'bani',
    'banr',
    'bori',
    'borr',
    'eqir',
    'eqri',
    'eqrr',
    'gtir',
    'gtri',
    'gtrr',
    'muli',
    'mulr',
    'seti',
    'setr',
)


def execute(opname: str, regs: tuple[int, ...], a: int, b: int, c: int):
    r = list(regs)
    match opname:
        case 'addr':
            r[c] = r[a] + r[b]
        case 'addi':
            r[c] = r[a] + b
        case 'mulr':
            r[c] = r[a] * r[b]
        case 'muli':
            r[c] = r[a] * b
        case 'banr':
            r[c] = r[a] & r[b]
        case 'bani':
            r[c] = r[a] & b
        case 'borr':
            r[c] = r[a] | r[b]
        case 'bori':
            r[c] = r[a] | b
        case 'setr':
            r[c] = r[a]
        case 'seti':
            r[c] = a
        case 'gtir':
            r[c] = int(a > r[b])
        case 'gtri':
            r[c] = int(r[a] > b)
        case 'gtrr':
            r[c] = int(r[a] > r[b])
        case 'eqir':
            r[c] = int(a == r[b])
        case 'eqri':
            r[c] = int(r[a] == b)
        case 'eqrr':
            r[c] = int(r[a] == r[b])
        case _:
            raise NotImplementedError('Unknown op:', opname)
    return tuple(r)


SAMPLES, TEST_PROGRAM = sys.stdin.read().split('\n\n\n')

a1 = 0

candidates = {n: set(OPNAMES) for n in range(16)}

for sample in SAMPLES.split('\n\n'):
    before, (opcode, a, b, c), after = [
        tuple(map(int, re.findall(r'\d+', d))) for d in sample.split('\n')
    ]

    ops = {opname for opname in OPNAMES if after == execute(opname, before, a, b, c)}
    candidates[opcode] &= ops
    a1 += len(ops) > 2

opcode_names = {}  # known assignments

while candidates:
    # identify unique opcode names
    for opcode, opset in list(candidates.items()):
        if len(opset) == 1:
            opcode_names[opcode] = opset.pop()
            del candidates[opcode]

    # remove already assigned names from other candidates
    for opcode, opset in candidates.items():
        candidates[opcode] -= set(opcode_names.values())

regs = (0, 0, 0, 0)
for line in TEST_PROGRAM.strip().split('\n'):
    op, a, b, c = map(int, line.split())
    regs = execute(opcode_names[op], regs, a, b, c)

print('part1:', a1)
print('part2:', a2 := regs[0])

assert a1 == 544
assert a2 == 600
