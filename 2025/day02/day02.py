import sys

a1 = a2 = 0

for g in sys.stdin.read().split(','):
    a, b = map(int, g.split('-'))
    for i in range(a, b + 1):
        s = str(i)
        a1 += i * (s == s[:len(s) // 2] * 2)
        a2 += i * (any(s == s[:i] * (len(s) // i) for i in range(1, len(s))))

print('part1:', a1)
print('part2:', a2)

assert a1 == 24043483400
assert a2 == 38262920235
