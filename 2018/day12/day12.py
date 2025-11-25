import re
import sys
from itertools import batched

state, *pairs = re.findall(r'[#.]+', sys.stdin.read())

rules = dict(batched(pairs, 2))


def step(state: str):
    if not state.startswith('..'):
        state = '..' + state
    if not state.endswith('..'):
        state += '..'

    vals = ['.'] * len(state)

    for i in range(len(state)):
        seg = state[i:i + 5]
        vals[i] = rules.get(seg, vals[i])

    # exit()

    return '....' + ''.join(vals).strip('.') + '....'


state = f'....{state}....'
gens = [state]
for _ in range(20):
    gens.append(state := step(state))

for i, s in enumerate(gens):
    # print(f'{i>2}: {s.ljust(".")}')
    print(f'{i:>2}: {s}')
