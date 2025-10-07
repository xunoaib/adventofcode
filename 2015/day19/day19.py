import re
import sys
from heapq import heappop, heappush

REPL_STRS, INPUT_STR = sys.stdin.read().strip().split('\n\n')
_REPLS = [s.split(' => ') for s in REPL_STRS.splitlines()]
REPLS: list[tuple[str, str]] = [(l, r) for l, r in _REPLS]
REV_REPLS = [(r, l) for l, r in REPLS]

repl_count = 0


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
    global repl_count

    pattern = r'Rn((?:(?!Rn|Ar|\(|\)).)*?)Ar'
    while m := re.search(pattern, s):
        segments = []
        for y in m.group(1).split('Y'):
            compressed = [
                v for v in reverse_to_one(y) if count_elements(v) == 1
            ]
            assert len(compressed) == 1
            seg = compressed[0]
            if y == seg:
                repl_count += 1  # TODO: must count reverse_to_one
            segments.append(seg)

        s = s[:m.start()] + '(' + 'Y'.join(segments) + ')' + s[m.end():]
    return s.replace('(', 'Rn').replace(')', 'Ar')


def replace_rnfyfars(s: str):
    global repl_count

    for l, r in [
        ('SiRnFYFAr', 'Ca'),
        ('NRnFYFAr', 'H'),
        ('SiRnMgAr', 'Ca'),
        ('NRnMgAr', 'H'),
    ]:
        if l in s:
            s = s.replace(l, r)
            repl_count += 1

    return s


def replace_rnars(s: str):
    for l, r in REPLS:
        if m := re.match(r'([A-Z][a-z]?)Rn(.*?)Ar', r):
            s = s.replace(m.group(), l)
    return s


def part2():
    s = INPUT_STR

    while 'Rn' in s:
        s = compress_inner_rn_ars(s)
        s = replace_rnfyfars(s)
        s = replace_rnars(s)
        s = s.replace('CRnFYMgAr', 'H')
        print('\n' + highlight(s))

    print(min(reverse_to_one(s), key=count_elements))
    print(repl_count)


# a1 = part1()
# print('part1:', a1)

a2 = part2()
# print('part2:', a2)

# assert a1 == 518
# assert a2 == ?
