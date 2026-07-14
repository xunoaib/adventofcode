aa = bb = None

n = int(input())

x = [3, 7]
i, j = 0, 1

for _ in range(n):
    x += [*map(int, str(x[i] + x[j]))]
    i = (i + x[i] + 1) % len(x)
    j = (j + x[j] + 1) % len(x)

while len(x) < n + 10:
    y = [*map(int, str(x[i] + x[j]))]
    x += y
    i = (i + x[i] + 1) % len(x)
    j = (j + x[j] + 1) % len(x)

print('part1:', aa := ''.join(map(str, x[n : n + 10])))

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
