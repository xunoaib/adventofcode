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


def part2():
    '''
    - collapse input -> e (instead of the other way around)?
    - prioritize big replacements over small
    - leverage low frequency of lowercase characters on certain sides (ie: n)
    - try to construct the string from left to right.
    - some chars are unique to the right (and cannot be replaced once created).
    - lowercase chars are never created on their own.
    '''

    pattern = r'Rn(.*?)Ar'
    s = input_str

    while m := re.search(pattern, s):
        repl = m.group(1)
        s = s[:m.start()] + s[m.end():]
        print(len(s), repl)

    print(s)

    return len(s)


def analyze():
    left = set(c for sr in repls for c in sr[0])
    right = set(c for sr in repls for c in sr[1])

    print('shared =', ''.join(sorted(left & right)))
    print('unique_r =', ''.join(sorted(right - left)))
    print('unique_l =', ''.join(sorted(left - right)))


# a1 = part1()
# print('part1:', a1)

a2 = part2()
# print('part2:', a2)

# assert a1 == 518
# assert a2 == ?
