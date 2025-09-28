banks = list(map(int, input().split()))

seen = {tuple(banks)}

a1 = 0
while True:
    blocks, idx = max((bank, -idx) for idx, bank in enumerate(banks))
    idx = abs(idx)
    a1 += 1

    banks[idx] = 0
    for i in range(blocks):
        banks[(idx + i + 1) % len(banks)] += 1

    t = tuple(banks)
    if t in seen:
        break

    seen.add(t)

print('part1:', a1)

seen = {tuple(banks)}

a1 = 0
while True:
    blocks, idx = max((bank, -idx) for idx, bank in enumerate(banks))
    idx = abs(idx)
    a1 += 1

    banks[idx] = 0
    for i in range(blocks):
        banks[(idx + i + 1) % len(banks)] += 1

    t = tuple(banks)
    if t in seen:
        break

    seen.add(t)

print('part2:', a1)
