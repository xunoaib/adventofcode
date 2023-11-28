#!/usr/bin/env python3
import sys

PUZTOPYOP = {
    'AND': '&',
    'OR': '|',
    'LSHIFT': '<<',
    'RSHIFT': '>>',
    'NOT': '~',
}

def line_to_code(line):
    lhs, rhs = line.split(' -> ')
    for srch, repl in PUZTOPYOP.items():
        lhs = lhs.replace(srch, repl)
    return f'{rhs}={lhs}'

def part1(codes):
    errors = True
    codes = set(codes)
    while errors:
        errors = False
        for code in codes.copy():
            try:
                exec(code)
                codes.remove(code)
            except NameError:
                errors = True
    return locals()['A']

def part2(codes, A):
    codes = [line for line in codes if not line.startswith('B=')]
    codes.append(f'B={A}')
    return part1(codes)

def main():
    lines = sys.stdin.read().strip().split('\n')
    codes = [line_to_code(line).upper() for line in lines]

    ans1 = part1(codes)
    print('part1:', ans1)

    ans2 = part2(codes, ans1)
    print('part2:', ans2)

    assert ans1 == 46065
    assert ans2 == 14134

if __name__ == '__main__':
    main()
