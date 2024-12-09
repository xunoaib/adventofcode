#!/usr/bin/env python3

nums = map(int, input())

num_files = 0
blocks = []

for i, v in enumerate(nums):
    isfile = not (i % 2)
    if isfile:
        for _ in range(v):
            blocks.append(num_files)
        num_files += 1
    else:
        for _ in range(v):
            blocks.append('.')

i = 0
j = len(blocks) - 1

while True:
    while blocks[i] != '.':
        i += 1
    while blocks[j] == '.':
        j -= 1

    if i >= j:
        break

    blocks[i], blocks[j] = blocks[j], blocks[i]

a1 = sum(i * int(n) for i, n in enumerate(blocks) if n != '.')

print('part1:', a1)

#  90180292337
