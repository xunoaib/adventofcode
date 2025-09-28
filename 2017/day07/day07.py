import re
import sys
from collections import defaultdict


def parse_input(data: str):
    lines = data.splitlines()

    weights: dict[str, int] = {}
    holding: dict[str, set[str]] = defaultdict(set)
    depends_on = defaultdict(set)

    for line in lines:
        if m := re.match(r'^(.*?) \((.*)\) -> (.*)$', line):
            l = m.group(1)
            rs = m.group(3).split(', ')
            holding[l]
            for r in rs:
                holding[r].add(l)
            weights[l] = int(m.group(2))
        elif m := re.search(r'^(.*?) \((.*)\)', line):
            l = m.group(1)
            holding[l]
            weights[l] = int(m.group(2))

    return weights, dict(holding)


def main():
    weights, holding = parse_input(sys.stdin.read())

    a1 = next(k for k, v in holding.items() if not v)

    print('part1:', a1)


if __name__ == '__main__':
    main()
