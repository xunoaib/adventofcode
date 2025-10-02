import re
import sys

repl_strs, input_str = sys.stdin.read().strip().split('\n\n')
repls = [s.split(' => ') for s in repl_strs.splitlines()]


def part1():
    distinct: set[str] = set()

    for srch, repl in repls:
        for m in re.finditer(srch, input_str):
            s = input_str[:m.start()] + repl + input_str[m.end():]
            distinct.add(s)

    return len(distinct)


a1 = part1()
print('part1:', a1)

assert a1 == 518
