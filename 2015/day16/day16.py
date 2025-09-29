import operator
import sys


def part1():
    candidates: list[int] = []

    for i, line in enumerate(lines):
        _, r = line.split(': ', 1)
        counts = [g.split(': ') for g in r.split(', ')]
        counts = {k: int(v) for k, v in counts}

        if all(v == LEGEND[k] for k, v in counts.items()):
            candidates.append(i + 1)

    assert len(candidates) == 1
    return candidates[0]


def part2():
    candidates: list[int] = []

    operators = {
        'cats': operator.gt,
        'trees': operator.gt,
        'pomeranians': operator.lt,
        'goldfish': operator.lt,
    }

    for i, line in enumerate(lines):
        _, r = line.split(': ', 1)
        counts = [g.split(': ') for g in r.split(', ')]
        counts = {k: int(v) for k, v in counts}

        if all(
            operators.get(k, operator.eq)(v, LEGEND[k])
            for k, v in counts.items()
        ):
            candidates.append(i + 1)

    assert len(candidates) == 1
    return candidates[0]


LEGEND = {
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
a2 = part2()

print('part1:', a1)
print('part2:', a2)
