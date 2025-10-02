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


def part2(molecule='e'):
    '''
    - collapse input -> e (instead of the other way around)?
    - prioritize big replacments over small
    - leverage low frequency of lowercase characters on certain sides (ie: n)
    '''


a1 = part1()
print('part1:', a1)

a2 = part2()
print('part2:', a2)

assert a1 == 518
# assert a2 == ?
