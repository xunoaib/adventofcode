from functools import cache
from hashlib import md5

aa = bb = None


@cache
def get_nlet(h: str, n: int):
    for i in range(len(h)):
        v = h[i:i + n]
        if v == v[0] * n:
            return v
    return ''


@cache
def gen_hash(idx):
    return md5(f'{salt}{idx}'.encode()).hexdigest()


@cache
def gen_hash2(idx):
    h = md5(f'{salt}{idx}'.encode()).hexdigest()
    for _ in range(2016):
        h = md5(h.encode()).hexdigest()
    return h


def part1():
    keys = []

    i = 0
    while len(keys) < 64:
        h = gen_hash(i)
        if v := get_nlet(h, 3):
            for j in range(i + 1, i + 1000):
                g = gen_hash(j)
                if v[0] * 5 in g:
                    # print(f'found key {i} {j} : {h} {g}')
                    keys.append(i)
                    break
        i += 1

    return str(keys[-1])


def part2():
    keys = []

    i = 0
    while len(keys) < 64:
        h = gen_hash2(i)
        if v := get_nlet(h, 3):
            for j in range(i + 1, i + 1001):
                g = gen_hash2(j)
                if v[0] * 5 in g:
                    print(f'found key {i} {j} : {h} {g}')
                    keys.append(i)
                    break
        i += 1

    return str(keys[-1])


salt = input()

# aa = part1()
bb = part2()

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
