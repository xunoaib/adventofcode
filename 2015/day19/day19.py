import re
import sys
from heapq import heappop, heappush

# WARN: Some strings are specific to my input. Adapt as needed.

# Hardcoded threshold to terminate BFS in a reasonable time
ABORT_BFS_THRESHOLD = 500

REPL_STRS, INPUT_STR = sys.stdin.read().strip().split('\n\n')
_REPLS = [s.split(' => ') for s in REPL_STRS.splitlines()]
REPLS: list[tuple[str, str]] = [(l, r) for l, r in _REPLS]
REV_REPLS = [(r, l) for l, r in REPLS]

# Number of replacements
a2_count = 0


def distinct_repls(input: str, repl_rules: list[tuple[str, str]]):
    distinct: set[str] = set()
    for srch, repl in repl_rules:
        for m in re.finditer(srch, input):
            s = input[:m.start()] + repl + input[m.end():]
            distinct.add(s)
    return distinct


def part1():
    return len(distinct_repls(INPUT_STR, REPLS))


def reverse_to_one(output: str):
    '''Compress a string into a single character with the fewest substitutions'''

    best = (float('inf'), None)
    q = [(count_elements(output), 0, output)]
    seen = {output}

    while q:
        n, steps, s = heappop(q)

        if n == 1:
            best = min(best, (steps, s))

        # Eagerly return the best result found if the search space is too large
        if len(seen) > ABORT_BFS_THRESHOLD and best[1] is not None:
            break

        if steps + 1 > best[0]:
            continue

        for t in distinct_repls(s, REV_REPLS):
            if t not in seen:
                heappush(q, (count_elements(t), steps + 1, t))
                seen.add(t)

    return best[1], best[0]


def count_elements(output: str):
    return sum(c.isupper() for c in output) + (output == 'e')


def highlight(s: str):
    s = re.sub(r'(Rn|Ar|C(?!a))', r'\033[93m\1\033[0m', s)
    return re.sub(r'(Y)', r'\033[91m\1\033[0m', s)


def compress_inner_rn_ars(s: str):
    global a2_count

    pattern = r'Rn((?:(?!Rn|Ar|\(|\)).)*?)Ar'
    while m := re.search(pattern, s):
        segments = []
        for y in m.group(1).split('Y'):
            compressed, steps = reverse_to_one(y)
            if compressed != y:
                a2_count += steps
            segments.append(compressed)
        s = s[:m.start()] + '(' + 'Y'.join(segments) + ')' + s[m.end():]
    return s.replace('(', 'Rn').replace(')', 'Ar')


def replace_rnfyfars(s: str):
    global a2_count

    for l, r in [
        ('SiRnFYFAr', 'Ca'),
        ('NRnFYFAr', 'H'),
        ('SiRnMgAr', 'Ca'),
        ('NRnMgAr', 'H'),
    ]:
        while l in s:
            s = s.replace(l, r, 1)
            a2_count += 1

    return s


def replace_rnars(s: str):
    global a2_count
    for l, r in REPLS:
        if m := re.match(r'([A-Z][a-z]?)Rn(.*?)Ar', r):
            while m.group() in s:
                s = s.replace(m.group(), l, 1)
                a2_count += 1
    return s


def part2():
    global a2_count
    s = INPUT_STR

    while 'Rn' in s:
        s = compress_inner_rn_ars(s)
        s = replace_rnfyfars(s)
        s = replace_rnars(s)

        while 'CRnFYMgAr' in s:
            s = s.replace('CRnFYMgAr', 'H', 1)
            a2_count += 1

        # print('\n' + highlight(s))

    s, steps = reverse_to_one(s)
    a2_count += steps

    assert s == 'e'
    return a2_count


print('WARN: These algorithms are (mostly) specific to my input')

a1 = part1()
print('part1:', a1)

a2 = part2()
print('part2:', a2)

assert a1 == 518
assert a2 == 200
