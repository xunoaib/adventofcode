#!/usr/bin/env python3
import sys
from z3 import Solver, Int


def main():
    lines = sys.stdin.read().strip().split('\n')

    val_to_char = {
        -2: '=',
        -1: '-',
        0: '0',
        1: '1',
        2: '2',
    }

    char_to_val = {v: k for k, v in val_to_char.items()}

    total = 0
    for line in lines:
        for i, ch in enumerate(line[::-1]):
            total += char_to_val[ch] * (5**i)

    print('total:', total)

    solver = Solver()
    digits = []

    for d in range(50):
        val = Int(str(d))
        digits.append(val)
        solver.add(-2 <= val)
        solver.add(val <= 2)

    ztotal = Int('total')
    solver.append(ztotal == total)
    solver.append(ztotal == sum(d * 5**p for p, d in enumerate(digits[::-1])))

    solver.check()
    model = solver.model()

    ans1 = ''
    for d in digits:
        val = model[d].as_long()
        ans1 += val_to_char[val]
    ans1 = ans1.lstrip('0')

    print('part1:', ans1)

    assert ans1 == '2-=102--02--=1-12=22'


if __name__ == '__main__':
    main()
