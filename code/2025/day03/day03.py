from itertools import combinations

lines = open(0).read().strip().split('\n')
a1 = a2 = 0

for line in lines:
    xs = list(map(int, list(line)))
    vals = sorted(enumerate(xs), key=lambda iv: (-iv[1], iv[0]))

    s = []
    for left in range(12, 0, -1):
        for i, v in vals:
            if i <= len(xs) - left:
                s.append(v)
                vals = [iv for iv in vals if iv[0] > i]
                break

    a1 += max(a * 10 + b for a, b in combinations(xs, r=2))
    a2 += int(''.join(map(str, s)))

print('part1:', a1)
print('part2:', a2)

assert a1 == 17301
assert a2 == 172162399742349
