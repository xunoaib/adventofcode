import re

s = re.sub(r'!.', '', input())

garbage = None
i = groups = a1 = a2 = 0

for i, c in enumerate(s):
    if garbage is not None:
        if c == '>':
            a2 += i - garbage - 1
            garbage = None
        i += 1
        continue
    if c == '{':
        groups += 1
    elif c == '<':
        garbage = i
    elif c == '}':
        a1 += groups
        groups -= 1
    i += 1

print('part1:', a1)
print('part2:', a2)

assert a1 == 14190
assert a2 == 7053
