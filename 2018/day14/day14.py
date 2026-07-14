def step(i, j):
    s = x[i] + x[j]
    if s >= 10:
        x.append(1)
        x.append(s - 10)
    else:
        x.append(s)
    i = (i + x[i] + 1) % len(x)
    j = (j + x[j] + 1) % len(x)
    return i, j


n = int(input())

x = bytearray([3, 7])
i, j = 0, 1

for _ in range(n):
    i, j = step(i, j)

while len(x) < n + 10:
    i, j = step(i, j)

print('part1:', aa := ''.join(map(str, x[n : n + 10])))

str_n = str(n)
str_len_n = len(str_n)
srch = bytearray(int(c) for c in str_n)

idx = x.find(srch)
while idx == -1:
    i, j = step(i, j)
    idx = x.find(srch, len(x) - str_len_n - 2)

print('part2:', bb := idx)

assert aa == '1031816654'
assert bb == 20179839
