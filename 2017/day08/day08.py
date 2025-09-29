import sys
from collections import Counter


def main():
    lines = sys.stdin.read().splitlines()

    regs = Counter()

    for line in lines:
        wreg, op, amt, _, lhs, cmp, rhs = line.split()
        amt = int(amt)
        rhs = int(rhs)
        op = '+' if op == 'inc' else '-'

        if eval(f'regs[{lhs!r}] {cmp} {rhs}'):
            exec(f'regs[{wreg!r}] {op}= {amt}')

    a1 = max(regs.values())
    print('part1:', a1)


if __name__ == '__main__':
    main()
