#!/usr/bin/env python3
import sys

def count_increases(lst):
    count = 0
    for i in range(len(lst)-1):
        if lst[i] < lst[i+1]:
            count += 1
    return count

def main():
    lines = sys.stdin.readlines()
    depths = list(map(int, lines))

    part1 = count_increases(depths)
    print('part1:', part1)
    assert part1 == 1696

    sums = []
    for i in range(len(depths)-2):
        sums.append(sum(depths[i:i+3]))

    part2 = count_increases(sums)
    print('part2:', part2)
    assert part2 == 1737

if __name__ == "__main__":
    main()
