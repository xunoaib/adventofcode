import re
import sys
from collections import defaultdict


def parse_input(data: str):
    lines = data.splitlines()

    weights = {}
    holding = defaultdict(set)

    for line in lines:
        if m := re.match(r'^(.*?) \((.*)\) -> (.*)$', line):
            l = m.group(1)
            r = m.group(3)
            holding[r] |= set(r.split(', '))
            weights[l] = int(m.group(2))
        elif m := re.search(r'^(.*?) \((.*)\)', line):
            l = m.group(1)
            weights[l] = int(m.group(2))

    return weights, dict(holding)


def main():
    weights, holding = parse_input(sys.stdin.read())


if __name__ == '__main__':
    main()
