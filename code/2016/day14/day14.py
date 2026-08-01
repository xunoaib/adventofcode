from functools import cache
from hashlib import md5


@cache
def get_nlet(h: str, n: int):
    for i in range(len(h)):
        v = h[i:i + n]
        if v == v[0] * n:
            return v
    return ''


@cache
def hash1(idx):
    return md5(f'{salt}{idx}'.encode()).hexdigest()


@cache
def hash2(idx):
    h = md5(f'{salt}{idx}'.encode()).hexdigest()
    for _ in range(2016):
        h = md5(h.encode()).hexdigest()
    return h


def solve(hash_func):
    keys = []
    i = 0
    while len(keys) < 64:
        if v := get_nlet(hash_func(i), 3):
            for j in range(i + 1, i + 1001):
                if v[0] * 5 in hash_func(j):
                    keys.append(i)
                    break
        i += 1
    return keys[-1]


salt = input()

a1 = solve(hash1)
print('part1:', a1)

a2 = solve(hash2)
print('part2:', a2)

assert a1 == 15035
assert a2 == 19968
