import re
import sys
from heapq import heappop, heappush

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


def reverse_to_one(output: str):
    '''This returns the first element that output can be compressed into (but
    is not guaranteed to be unique)'''

    q = [(count_elements(output), output)]
    seen = {output}
    while q:
        n, s = heappop(q)
        if n == 1:
            return [s]
        for t in distinct_repls(s, REV_REPLS):
            if t not in seen:
                heappush(q, (count_elements(t), t))
                seen.add(t)
    return seen


def count_elements(output: str):
    return sum(c.isupper() for c in output)


def highlight(s: str):
    s = re.sub(r'(Rn|Ar|C(?!a))', r'\033[93m\1\033[0m', s)
    return re.sub(r'(Y)', r'\033[91m\1\033[0m', s)


def compress_inner_rn_ars(s: str):
    # pattern = r'Rn((?:(?!Rn|Ar|\.\.\.).)*?)Ar'
    pattern = r'Rn((?:(?!Rn|Ar|\(|\)).)*?)Ar'
    while m := re.search(pattern, s):
        segments = []
        for y in m.group(1).split('Y'):
            compressed = [
                v for v in reverse_to_one(y) if count_elements(v) == 1
            ]
            assert len(compressed) == 1
            segments.append(compressed[0])
        s = s[:m.start()] + '(' + 'Y'.join(segments) + ')' + s[m.end():]
    return s.replace('(', 'Rn').replace(')', 'Ar')


def replace_rnfyfars(s: str):
    s = s.replace('SiRnFYFAr', 'Ca')
    s = s.replace('NRnFYFAr', 'H')
    s = s.replace('SiRnMgAr', 'Ca')
    s = s.replace('NRnMgAr', 'H')
    return s


def replace_rnars(s: str):
    for l, r in REPLS:
        if m := re.match(r'([A-Z][a-z]?)Rn(.*?)Ar', r):
            s = s.replace(m.group(), l)
    return s


def part2():
    s = INPUT_STR

    # Compress innermost Rn..Ar segments into single molecules
    s = compress_inner_rn_ars(s)
    print('\n' + highlight(s))

    s = replace_rnfyfars(s)
    s = replace_rnars(s)
    print('\n' + highlight(s))

    s = compress_inner_rn_ars(s)
    print('\n' + highlight(s))

    s = replace_rnfyfars(s)
    print('\n' + highlight(s))

    s = replace_rnars(s)
    print('\n' + highlight(s))

    s = compress_inner_rn_ars(s)
    print('\n' + highlight(s))

    s = s.replace('CRnFYMgAr', 'H')
    print('\n' + highlight(s))

    print(min(reverse_to_one(s), key=count_elements))

    exit()

    # gs = [g for g in re.split(r'([A-Z][a-z]?)', s) if g]
    # gs = [g for g in re.split(r'((?:(?!Rn|Ar|\(|\)).)*?)Ar', s) if g]
    gs = [g for g in re.split(r'(Rn|Ar|Y)', s) if g]
    # print(gs)

    output = []
    for g in gs:
        compressed = [v for v in reverse(g) if count_elements(v) == 1]
        if g in ('Rn', 'Ar', 'Y'):
            output.append(g)
            continue

        if len(compressed) == 1:
            # print(g, '=>', compressed)
            output.append(compressed[0])
        else:
            # print(g, '=>', 'no compression')
            output.append(g)

    s = ''.join(output)
    print('\n' + highlight(s))
    exit()

    # # Compress isolated segments into single molecules
    # pattern = r'Rn((?:(?!Rn|Ar|\(|\)).)*?)Ar'
    # while m := re.search(pattern, s):
    #     ys = m.group(1).split('Y')
    #     segments = []
    #     for y in ys:
    #         compressed = [v for v in reverse(y) if count_elements(v) == 1]
    #         assert len(compressed) == 1
    #         segments.append(compressed[0])
    #     s = s[:m.start()] + '(' + 'Y'.join(segments) + ')' + s[m.end():]

    s = s.replace('(', 'Rn').replace(')', 'Ar')
    print(highlight(s))

    print(s)
    print()

    s = s.replace('(', 'Rn').replace(')', 'Ar')
    print(highlight(s))
    exit()

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

    # TODO:
    # - Now find and perform candidate Rn/Ar substitutions (those with 100% certainty)
    # - Consider partial Rn/Ar template matches to deduce further constraints.

    print('\nHardened:')
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
