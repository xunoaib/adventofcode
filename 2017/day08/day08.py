import sys
from collections import Counter


def main():
    a2 = 0
    regs = Counter()

    for line in sys.stdin:
        wreg, op, amt, _, lhs, cmp, rhs = line.split()
        amt = int(amt)
        rhs = int(rhs)
        op = '+' if op == 'inc' else '-'

        if eval(f'regs[{lhs!r}] {cmp} {rhs}'):
            exec(f'regs[{wreg!r}] {op}= {amt}')
            a2 = max(regs[wreg], a2)

    a1 = max(regs.values())

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 8022
    assert a2 == 9819


if __name__ == '__main__':
    main()
