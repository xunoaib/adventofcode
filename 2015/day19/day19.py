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
    # pattern = r'^(.*)Rn(.*?)Ar(.*)$'
    # pattern = r'Rn(.*?)Ar'
    pattern = r'Rn((?:(?!Rn|Ar).)*?)Ar'
    s = input_str

    last_s = s
    while m := re.search(pattern, s):
        x = m.groups(1)[0]
        # s = s[:m.start()] + 'Rn...Ar' + s[m.end():]
        s = s[:m.start()] + '...' + s[m.end():]
        # print(len(s), m)
        print(x)
        # print(s)

        # if s == last_s:
        #     break
        # last_s = s

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
