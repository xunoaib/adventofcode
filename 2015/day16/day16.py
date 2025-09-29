import sys

legend = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

lines = sys.stdin.read().splitlines()

candidates = []

for i, line in enumerate(lines):
    l, r = line.split(': ', 1)
    counts = [g.split(': ') for g in r.split(', ')]
    counts = {k: int(v) for k, v in counts}

    if all(v == legend[k] for k, v in counts.items()):
        candidates.append(i + 1)

assert len(candidates) == 1

a1 = candidates[0]

print('part1:', a1)
