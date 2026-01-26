def is_open(x, y):
    v = N + x * x + 3 * x + 2 * x * y + y + y * y
    return f'{v:b}'.count('1') % 2 == 0


def neighbors4(r, c):
    return {(r + dr, c + dc) for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]}


def bfs(src, tar):
    q = [(0, src)]
    seen = {src}
    while q:
        cost, p = q.pop(0)
        if p == tar:
            return cost
        for n in neighbors4(*p):
            if n not in seen and is_open(*n):
                q.append((cost + 1, n))
                seen.add(n)
    assert False


aa = bb = None

N = int(input())

src = (1, 1)
tar = (31, 39)

aa = bfs(src, tar)

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

assert aa == 90
# assert bb == 0
