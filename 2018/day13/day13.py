import sys


def find_in_dir(r: int, c: int, dr: int, dc: int, src: str, tar: str):
    assert grid[r, c] == src
    while grid[r, c] != tar:
        r += dr
        c += dc
    return r, c


def find_right(r, c):
    return find_in_dir(r, c, 0, 1, '/', '\\')


def find_left(r, c):
    return find_in_dir(r, c, 0, -1, '/', '\\')


def find_down(r, c):
    return find_in_dir(r, c, 1, 0, '\\', '/')


def find_up(r, c):
    return find_in_dir(r, c, -1, 0, '\\', '/')


def points_between(p1, p2, include_last=False):
    r1, c1 = p1
    r2, c2 = p2

    dr = (r2 > r1) - (r2 < r1)
    dc = (c2 > c1) - (c2 < c1)

    assert 0 in (dr, dc)

    points = [(r1, c1)]
    while (r1, c1) != p2:
        r1 += dr
        c1 += dc
        points.append((r1, c1))

    if not include_last:
        points.pop()
    return points


aa = bb = None

lines = sys.stdin.read().split('\n')

grid = {(r, c): ch for r, line in enumerate(lines) for c, ch in enumerate(line)}

carts = {p for p, v in grid.items() if v in '^v<>'}
corners = {p for p, v in grid.items() if v in r'\/'}
intersections = {p for p, v in grid.items() if v in r'+'}
print(len(carts))

ul_corners = {
    (r, c) for (r, c), v in grid.items() if v == '/' and grid.get((r, c + 1)) == '-'
}


print(ul_corners)

rings = []

for p in ul_corners:
    # print(p, grid[p])
    # print(p := find_right(*p), grid[p])
    # print(p := find_down(*p), grid[p])
    # print(p := find_left(*p), grid[p])
    # print(p := find_up(*p), grid[p])
    # print()

    funcs = [find_right, find_down, find_left, find_up]
    points = []

    for f in funcs:
        q = f(*p)
        points += points_between(p, q)
        p = q

    print(p, len(points), points)


# if ch in r'\/'

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
