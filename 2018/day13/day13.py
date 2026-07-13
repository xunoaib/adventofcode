import sys
from collections import defaultdict

# TODO:
# - identify track sections (top, right, bottom, left) and "facing" directions on each section

DIRS4 = R, D, L, U = (0, 1), (1, 0), (0, -1), (-1, 0)

FACING_R, FACING_D, FACING_L, FACING_U = range(4)


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


def get_track_dir(
    pos: tuple[int, int],
    true_facing_dir: int,
    track: list[tuple[int, int]],
):
    section = track.index(pos) // (len(track) // 4)
    return {
        (0, FACING_R): 1,
        (0, FACING_L): -1,
        (1, FACING_D): 1,
        (1, FACING_U): -1,
        (2, FACING_R): -1,
        (2, FACING_L): 1,
        (3, FACING_D): -1,
        (3, FACING_U): 1,
    }[section, true_facing_dir]


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

# carts = {p for p, v in grid.items() if v in '^v<>'}
# corners = {p for p, v in grid.items() if v in r'\/'}
# intersections = {p for p, v in grid.items() if v in r'+'}

ul_corners = {
    (r, c)
    for (r, c), v in grid.items()
    if v == '/' and grid.get((r, c + 1), 'X') in '-+'
}

tracks = []
carts = []

tile_track_ids = defaultdict(list)

for track_id, src in enumerate(ul_corners):
    funcs = [find_right, find_down, find_left, find_up]
    dirs = '>v<^'
    points = []

    for next_corner, dir_char in zip(funcs, dirs):
        tar = next_corner(*src)
        add = points_between(src, tar)

        for p in add:
            # associate track tile with track id
            tile_track_ids[p].append(track_id)

            # identify cart
            if (cart_char := grid[p]) in dirs:
                track_dir = 1 if cart_char == dir_char else -1
                turn_state = -1  # next turn dir (left)
                facing_dir = dirs.index(cart_char)
                carts.append((p, track_dir, track_id, turn_state, facing_dir))

        points += add
        src = tar

    tracks.append(points)


def step_cart():
    print('\n=== STEP ===\n')
    global carts

    new_carts = []

    # step carts foward
    for pos, track_dir, track_id, turn_state, facing_dir in carts:
        track = tracks[track_id]
        i = track.index(pos)
        npos = track[(i + track_dir) % len(track)]
        print('>>> track', track_id, pos, '->', npos, 'tracks:', tile_track_ids[npos])

        if grid[npos] == '+':
            print('--- intersection ---')
            if turn_state:  # left/right turn, swap tracks
                print('--- switching tracks ---')
                track_id = next(t for t in tile_track_ids[npos] if t != track_id)

            print('old facing', facing_dir)
            new_facing_dir = (facing_dir + turn_state) % 4
            print('new facing', new_facing_dir)
            # print(DIRS4[new_facing_dir])

            turn_state = (turn_state + 2) % 3 - 1
            print('new turn state:', turn_state)

            x = get_track_dir(npos, new_facing_dir, tracks[track_id])
            print('track_dir:', x)

        new_carts.append((npos, track_dir, track_id, turn_state, facing_dir))

    carts = new_carts


step_cart()
step_cart()


if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
