aa = bb = None

n = int(input())

x = [3, 7]
i, j = 0, 1

for _ in range(n):
    x += [*map(int, str(x[i] + x[j]))]
    i = (i + x[i] + 1) % len(x)
    j = (j + x[j] + 1) % len(x)

while len(x) < n + 10:
    x += [*map(int, str(x[i] + x[j]))]
    i = (i + x[i] + 1) % len(x)
    j = (j + x[j] + 1) % len(x)

s = ''.join(map(str, x))

print('part1:', aa := s[n : n + 10])

last_idx = 0
while str(n) not in s:
    last_idx = len(x) - len(str(n))
    x += [*map(int, str(x[i] + x[j]))]
    i = (i + x[i] + 1) % len(x)
    j = (j + x[j] + 1) % len(x)
    s = ''.join(map(str, x[last_idx:]))

print('part2:', bb := last_idx + s.index(str(n)))

assert aa == '1031816654'
assert bb == 20179839
