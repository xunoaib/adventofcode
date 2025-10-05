import re
import sys

REPL_STRS, INPUT_STR = sys.stdin.read().strip().split('\n\n')
_REPLS = [s.split(' => ') for s in REPL_STRS.splitlines()]
REPLS: list[tuple[str, str]] = [(l, r) for l, r in _REPLS]
REV_REPLS = [(r, l) for l, r in REPLS]


def distinct_repls(input: str, repl_rules: list[tuple[str, str]]):
    distinct: set[str] = set()
    for srch, repl in repl_rules:
        for m in re.finditer(srch, input):
            s = input[:m.start()] + repl + input[m.end():]
            distinct.add(s)
    return distinct


def part1():
    return len(distinct_repls(INPUT_STR, REPLS))


def reverse(output: str):
    q = [output]
    seen = {output}
    while q:
        s = q.pop()
        for t in distinct_repls(s, REV_REPLS):
            if t not in seen:
                q.append(t)
                seen.add(t)
    return seen


def count_elements(output: str):
    return sum(c.isupper() for c in output)


def part2():
    pattern = r'Rn((?:(?!Rn|Ar|\.\.\.).)*?)Ar'
    s = INPUT_STR

    while m := re.search(pattern, s):
        y = m.group(1)
        y_segments = []

        for x in y.split('Y'):
            rs = reverse(x)
            min_vals = [v for v in rs if count_elements(v) == 1]
            min_val = (min_vals + [x])[0]
            assert len(min_vals) <= 1

            if x == min_val:
                # print(f'L1: {len(min_vals)}   {x} unchanged')
                pass
            else:
                print(
                    # f'Min: {min_caps} ({len(min_vals)})  N: {len(rs):>3}    {x} => {min_val}'
                    f'L1: {len(min_vals)}   {x} => {min_val}'
                )
            y_segments.append(min_val)

        s = s[:m.start()] + '(' + 'Y'.join(y_segments) + ')' + s[m.end():]

    print()
    print(s)

    t = s.replace('(', 'Rn').replace(')', 'Ar')
    print('\nAfter:')
    print(t)

    print('\nBefore:')
    print(INPUT_STR)

    return len(s)


# a1 = part1()
# print('part1:', a1)

a2 = part2()
# print('part2:', a2)

# assert a1 == 518
# assert a2 == ?
