import re
import sys

OPS = (
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


def execute(op: str, regs: tuple[int, ...], a: int, b: int, c: int):
    r = list(regs)
    match op:
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
            raise NotImplementedError('Unknown op:', op)
    return tuple(r)


aa = bb = None

data = sys.stdin.read()

g1, g2 = data.split('\n\n\n')

aa = 0

for log in g1.split('\n\n'):
    before, (opcode, a, b, c), after = [
        tuple(map(int, re.findall(r'\d+', l))) for l in log.split('\n')
    ]
    print(before, (opcode, a, b, c), after)

    candidates = []
    for opname in OPS:
        if after == execute(opname, before, a, b, c):
            candidates.append(opname)
    print(candidates)
    aa += len(candidates) > 2


# for line in g2.strip().split('\n'):
#     opname, a, b, c = map(int, line.split())

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
