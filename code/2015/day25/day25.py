import re

tr, tc = map(int, re.findall(r'\d+', input()))

a1 = 20151125
r = c = 1

while (r, c) != (tr, tc):
    r -= 1
    c += 1
    if r < 1:
        r, c = c, 1

    a1 = (a1 * 252533) % 33554393

print('part1:', a1)

assert a1 == 9132360
