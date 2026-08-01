#!/usr/bin/env python3
import re
import sys

from z3 import Int, Solver

def solve(lines: list, part2: bool):
    solver = Solver()
    monkeys = {}

    for line in lines:
        name, value = re.match('(.*): (.*)', line).groups()
        monkeys[name] = Int(name)

    for line in lines:
        name, value = re.match('(.*): (.*)', line).groups()

        if name == 'humn' and part2:
            continue

        if value.isdigit():
            solver.add(monkeys[name] == int(value))
            continue

        lhs, op, rhs = value.split(' ')
        m = monkeys[name]
        a = monkeys[lhs]
        b = monkeys[rhs]

        if name == 'root' and part2:
            solver.add(a == b)
            continue

        if op == '-':
            solver.add(m == a - b)
        elif op == '+':
            solver.add(m == a + b)
        elif op == '/':
            solver.add(m == a / b)
            solver.add(a % b == 0)
        elif op == '*':
            solver.add(m == a * b)

    solver.check()
    model = solver.model()

    if part2:
        return model[monkeys['humn']].as_long()
    else:
        return model[monkeys['root']].as_long()

def main():
    lines = sys.stdin.read().strip().split('\n')

    ans1 = solve(lines, part2=False)
    ans2 = solve(lines, part2=True)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 155708040358220
    assert ans2 == 3342154812537

if __name__ == '__main__':
    main()
