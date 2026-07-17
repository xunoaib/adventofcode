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


aa = bb = None

data = sys.stdin.read()

g1, g2 = data.split('\n\n\n')

aa = 0

multi_candidates = defaultdict(list)

for log in g1.split('\n\n'):
    before, (opcode, a, b, c), after = [
        tuple(map(int, re.findall(r'\d+', l))) for l in log.split('\n')
    ]

    ops = {opname for opname in OPNAMES if after == execute(opname, before, a, b, c)}
    multi_candidates[opcode].append(ops)
    aa += len(ops) > 2

opcode_names = {}
candidates = {}

# find the intersection of possibilities for each opcode
for opcode, opsets in multi_candidates.items():
    intersect = set(OPNAMES)
    grp = opsets.copy()
    while grp:
        intersect &= grp.pop()
    candidates[opcode] = intersect

while candidates:
    # identify unique opcode names
    for opcode, opset in list(candidates.items()):
        if len(opset) == 1:
            opcode_names[opcode] = [*opset][0]
            del candidates[opcode]

    # remove already assigned names from other candidates
    for opcode, opset in candidates.items():
        candidates[opcode] -= set(opcode_names.values())

print(opcode_names)
for k, v in sorted(opcode_names.items()):
    print(k, v)

regs = (0, 0, 0, 0)
for g in g2.strip().split('\n'):
    op, a, b, c = map(int, g.split())
    regs = execute(opcode_names[op], regs, a, b, c)

bb = regs[0]

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
