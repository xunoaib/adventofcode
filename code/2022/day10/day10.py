#!/usr/bin/env python3
import re
import sys

def main():
    data = sys.stdin.read().strip()
    data = re.sub(r'addx', 'noop\naddx', data)
    lines = data.split('\n')

    x = 1
    ans1 = 0
    pixels = ''

    for cycle, line in enumerate(lines, start=1):
        if cycle >= 20 and (cycle - 20) % 40 == 0:
            ans1 += cycle * x

        r, c = divmod(cycle - 1, 40)
        if c == 0:
            pixels += '\n'
        pixels += '#' if abs(x - c) <= 1 else '.'

        if line != 'noop':
            x += int(line.split(' ')[1])

    print('part1:', ans1)
    print('part2: ZKJFBJFZ')
    print(pixels)

    assert ans1 == 12840


if __name__ == '__main__':
    main()
