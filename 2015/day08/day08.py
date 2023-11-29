#!/usr/bin/env python3
import ast
import sys

def part1(lines):
    mems = list(map(ast.literal_eval, lines))
    return sum(map(len, lines)) - sum(map(len, mems))

def part2(lines):
    count = 0
    for line in lines:
        count += 2 + len(line.replace('\\', '\\\\').replace('"','\\"'))
    return count - sum(map(len, lines))

def main():
    lines = sys.stdin.read().strip().split('\n')

    ans1 = part1(lines)
    print('part1:', ans1)

    ans2 = part2(lines)
    print('part2:', ans2)

    assert ans1 == 1333
    assert ans2 == 2046

if __name__ == '__main__':
    main()
