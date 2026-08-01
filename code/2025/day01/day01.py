a1 = a2 = 0
dial = 50

for line in open(0):
    dir = line[0]
    count = int(line[1:])

    for _ in range(count):
        dial = (dial + (-1)**(dir == 'R')) % 100
        a2 += not dial

    a1 += not dial

print('part1:', a1)
print('part2:', a2)

assert a1 == 1084
assert a2 == 6475
