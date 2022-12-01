#!/usr/bin/env python3
import sys

def main():
    groups = sys.stdin.read().strip().split('\n\n')
    calories = sorted(sum(map(int, g.split('\n'))) for g in groups)

    part1 = max(calories)
    print('part1:', part1)
    assert part1 == 67622

    part2 = sum(calories[-3:])
    print('part2:', part2)
    assert part2 == 201491


if __name__ == "__main__":
    main()
