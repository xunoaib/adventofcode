import re

s = input()
s = re.sub(r'!.', '', s)

i = 0
garbage = None
groups = []

aa = bb = 0

for c in s:
    if garbage is not None:  # in_garbage
        if c == '>':
            print('closing garbage')
            garbage = None
        i += 1
        continue

    if c == '{':
        groups.append(i)
        print('new group', groups)
    elif c == '<':
        print('new garbage')
        garbage = i
    elif c == '}':
        print('closing group', groups, len(groups))
        aa += len(groups)
        groups.pop()

    i += 1

print('part1:', aa)
print('part2:', bb)

assert aa == 14190
