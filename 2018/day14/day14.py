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

while len(x) < n + 10:
    i, j = step(i, j)

print('part1:', a1 := ''.join(map(str, x[n : n + 10])))

n_str = str(n)
len_n = len(n_str)
srch = bytearray(map(int, str(n)))

idx = x.find(srch)
while idx == -1:
    i, j = step(i, j)
    idx = x.find(srch, len(x) - len_n - 2)

print('part2:', a2 := idx)

assert a1 == '1031816654'
assert a2 == 20179839
