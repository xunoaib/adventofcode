import sys


def part1():
    candidates: list[int] = []

    for i, line in enumerate(lines):
        l, r = line.split(': ', 1)
        counts = [g.split(': ') for g in r.split(', ')]
        counts = {k: int(v) for k, v in counts}

        if all(v == legend[k] for k, v in counts.items()):
            candidates.append(i + 1)

    assert len(candidates) == 1

    return candidates[0]


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

a1 = part1()

print('part1:', a1)
