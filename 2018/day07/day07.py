import sys
from collections import defaultdict


def find_candidates(deps: dict[str, set[str]]):
    return sorted(k for k, v in deps.items() if not v)


def part1(deps):
    s = ''
    while deps:
        c = find_candidates(deps)[0]
        s += c

        del deps[c]
        for k, v in deps.items():
            v.discard(c)
    return s


def main():
    deps: dict[str, set[str]] = defaultdict(set)

    for line in sys.stdin:
        args = line.split()
        a, b = args[1], args[-3]
        deps[a]
        deps[b].add(a)

    a1 = part1(dict(deps))

    print('part1:', a1)


if __name__ == '__main__':
    main()
