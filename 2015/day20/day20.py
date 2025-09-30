from collections import Counter

n = int(input())

maxelf = n // 10 + 1  #??

presents = Counter()
for elf in range(1, maxelf):
    for house in range(elf, maxelf, elf):
        presents[house] += 10 * elf

a1 = min(house for house, count in presents.items() if count >= n)
print('part1:', a1)
