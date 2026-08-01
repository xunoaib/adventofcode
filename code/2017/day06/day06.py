def find_loop(banks):
    seen = {tuple(banks)}
    steps = 0
    while True:
        blocks, idx = max((bank, -idx) for idx, bank in enumerate(banks))
        idx = abs(idx)
        steps += 1

        banks[idx] = 0
        for i in range(blocks):
            banks[(idx + i + 1) % len(banks)] += 1

        t = tuple(banks)
        if t in seen:
            break

        seen.add(t)

    return steps


banks = list(map(int, input().split()))

a1 = find_loop(banks)
a2 = find_loop(banks)

print('part1:', a1)
print('part2:', a2)

assert a1 == 14029
assert a2 == 2765
