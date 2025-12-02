import sys


def invalid1(s: str):
    return s[:len(s) // 2] * 2 == s


def invalid2(s: str):
    return any(s[:i] * (len(s) // i) == s for i in range(1, len(s)))


a1 = a2 = 0

for g in sys.stdin.read().split(','):
    a, b = map(int, g.split('-'))
    for i in range(a, b + 1):
        a1 += i * invalid1(str(i))
        a2 += i * invalid2(str(i))

print('part1:', a1)
print('part2:', a2)

assert a1 == 24043483400
assert a2 == 38262920235
