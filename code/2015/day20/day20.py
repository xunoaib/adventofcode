N = int(input())
MAXELF = N // 10 + 1  #??


def part1():
    presents = [0] * MAXELF
    for elf in range(1, MAXELF):
        for house in range(elf, MAXELF, elf):
            presents[house] += 10 * elf

    return next(house for house, count in enumerate(presents) if count >= N)


def part2():
    presents = [0] * MAXELF
    for elf in range(1, MAXELF):
        houseshit = 0
        for house in range(elf, MAXELF, elf):
            presents[house] += 11 * elf
            houseshit += 1
            if houseshit >= 50:
                break

    return next(house for house, count in enumerate(presents) if count >= N)


a1 = part1()
a2 = part2()

print('part1:', a1)
print('part2:', a2)

assert a1 == 786240
assert a2 == 831600
