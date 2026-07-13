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

for p in ul_corners:
    print(p, grid[p])
    print(p := find_right(*p), grid[p])
    print(p := find_down(*p), grid[p])
    print(p := find_left(*p), grid[p])
    print(p := find_up(*p), grid[p])
    print()

# if ch in r'\/'

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
