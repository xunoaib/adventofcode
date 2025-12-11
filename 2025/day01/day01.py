import sys

dial = 50
a1 = a2 = 0

for line in sys.stdin:
    dir = line[0]
    count = int(line[1:])
    offset = 1 if dir == 'R' else -1

    for _ in range(count):
        dial += offset
        dial %= 100
        a2 += not dial

    a1 += not dial

print('part1:', a1)
print('part2:', a2)

assert a1 == 1084
assert a2 == 6475
