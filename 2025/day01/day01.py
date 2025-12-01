import sys

dial = 50
a1 = a2 = 0

for line in sys.stdin:
    dir = line[0]
    count = int(line[1:])

    offset = 1 if dir == 'R' else -1

    for _ in range(count):
        dial = (dial + offset) % 100
        if dial == 0:
            a2 += 1

    if dial == 0:
        a1 += 1

print('part1:', a1)
print('part2:', a2)

assert a1 == 1084
assert a2 == 6475
