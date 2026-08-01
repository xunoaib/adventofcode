#!/usr/bin/env python3
import re
import sys

def main():
    lines = sys.stdin.read().strip().split('\n')

    stacks = [[] for _ in range(9)]
    for line in lines[:8]:
        for i in range(1, len(line), 4):
            if line[i] != ' ':
                stacks[(i-1)//4].insert(0, line[i])

    for command in lines[10:]:
        num, src, tar = map(int, re.match('move (.*) from (.*) to (.*)', command).groups())
        for _ in range(num):
            stacks[tar-1].append(stacks[src-1].pop())

    tops1 = ''.join(stack[-1] for stack in stacks)
    print('part1:', tops1)

    stacks = [[] for _ in range(9)]
    for line in lines[:8]:
        for i in range(1, len(line), 4):
            if line[i] != ' ':
                stacks[(i-1)//4].insert(0, line[i])

    for command in lines[10:]:
        num, src, tar = map(int, re.match('move (.*) from (.*) to (.*)', command).groups())
        stacks[tar-1] += stacks[src-1][-num:]
        stacks[src-1] = stacks[src-1][:-num]

    tops2 = ''.join(stack[-1] for stack in stacks)
    print('part2:', tops2)

    assert tops1 == 'TGWSMRBPN'
    assert tops2 == 'TZLTLWRNF'

if __name__ == '__main__':
    main()
