def isfresh(i):
    return any(a <= i <= b for a, b in newranges)


s, b = open(0).read().split('\n\n')

ranges = sorted(tuple(map(int, line.split('-'))) for line in s.split('\n'))
newranges = [ranges.pop(0)]

while ranges:
    s1, e1 = newranges[-1]
    s2, e2 = ranges.pop(0)
    s = max(s2, e1)
    s += e1 == s
    if s <= e2:
        newranges.append((s, e2))

a1 = sum(map(isfresh, map(int, b.splitlines())))
a2 = sum((e - s + 1) for s, e in newranges)

print('part1:', a1)
print('part2:', a2)

assert a1 == 756
assert a2 == 355555479253787
