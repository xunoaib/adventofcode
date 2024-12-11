#!/usr/bin/env python3


import sys
from functools import cache

stones = tuple(map(int, input().split()))

# for i in range(25):
#     new = []
#     for s in stones:
#         if s == 0:
#             new.append(1)
#         elif len(str(s)) % 2 == 0:
#             t = str(s)
#             new += [int(t[:len(t)//2]), int(t[len(t)//2:])]
#         else:
#             new.append(s * 2024)
#     stones = new
# x = len(stones)
# print('part1:', x)

@cache
def split(num, d):
    # print(d, num)
    if d == 0:
        return [num]

    if num == 0:
        return [v for v in split(1, d-1)]
    elif len(str(num)) % 2 == 0:
        t = str(num)
        a,b = [int(t[:len(t)//2]), int(t[len(t)//2:])]
        vs1 = [v for v in split(a, d-1)]
        vs2 = [v for v in split(b, d-1)]
        return vs1+vs2
    else:
        return [v for v in split(num * 2024, d-1)]

r = []
for i,n in enumerate(stones):
    print(i,n)
    r += split(n, 75)

a2 = len(r)
print('part2:', a2)

# print('part1:', a1)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
