import re
import sys
from itertools import batched

state, *pairs = re.findall(r'[#.]+', sys.stdin.read())

rules = dict(batched(pairs, 2))


def step(state: str, idx: int):
    while not state.startswith('....'):
        state = '.' + state
        idx += 1

    while not state.endswith('....'):
        state += '.'

    vals = ['.'] * len(state)

    for i in range(len(state)):
        seg = state[i - 2:i + 3]
        vals[i] = rules.get(seg, vals[i])

    return ''.join(vals).rstrip('.'), idx


def pot_nums(state, idx):
    return [idx for idx, v in enumerate(state, start=-idx) if v == '#']


gens = [(f'....{state}....', 4)]
for _ in range(20):
    gens.append(step(*gens[-1]))

for i, (s, idx) in enumerate(gens):
    print(f'{i:>2}: ({idx:>3}) {s}')
    print(pot_nums(s, idx))

print('part1:', sum(pot_nums(*gens[-1])))
