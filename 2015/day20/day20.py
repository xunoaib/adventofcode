from collections import Counter

N = int(input())
MAXELF = N // 10 + 1  #??


def part1(n):
    presents = Counter()
    for elf in range(1, MAXELF):
        for house in range(elf, MAXELF, elf):
            presents[house] += 10 * elf
    return min(house for house, count in presents.items() if count >= n)


def part2(n):
    presents = Counter()
    for elf in range(1, MAXELF):
        houseshit = 0
        for house in range(elf, MAXELF, elf):
            presents[house] += 11 * elf
            houseshit += 1
            if houseshit >= 50:
                break

    return min(house for house, count in presents.items() if count >= n)


a1 = part1(N)
a2 = part2(N)

print('part1:', a1)
print('part2:', a2)

assert a1 == 786240
assert a2 == 831600
