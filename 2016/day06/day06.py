#!/usr/bin/env python3
import sys
from collections import Counter


def main():
    lines = sys.stdin.read().strip().splitlines()

    counters = [Counter() for _ in range(len(lines[0]))]
    for line in lines:
        for i, ch in enumerate(line):
            counters[i][ch] += 1

    part1 = ''.join(counter.most_common()[0][0] for counter in counters)
    print('part1:', part1)

    part2 = ''.join(counter.most_common()[-1][0] for counter in counters)
    print('part2:', part2)


if __name__ == "__main__":
    main()
