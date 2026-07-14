# NOTE: Very messy

import sys
from collections import defaultdict
from dataclasses import dataclass

DIRS4 = R, D, L, U = (0, 1), (1, 0), (0, -1), (-1, 0)


@dataclass
class Cart:
    track_id: int
    track_pos: int  # position on track
    facing_forward: int  # direction on track (1=forward, -1=backward)
    turn_state: int  # next turn ID (-1, 0, 1)


def print_grid():
    maxr = max(r for r, c in grid)
    maxc = max(c for r, c in grid)

    cart_dirs = {*map(cart_coords, carts)}

    print()
    for r in range(maxr + 1):
        for c in range(maxc + 1):
            ch = grid[r, c]
            if (r, c) in cart_dirs:
                ch = '\033[91mX\033[0m'
            print(ch, end='')
        print()
    print()


def cart_coords(cart: Cart):
    return tracks[cart.track_id][cart.track_pos]


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


def step_cart(cart: Cart):
    track_id = cart.track_id
    track = tracks[track_id]

    pos = track[cart.track_pos]
    npos = track[(cart.track_pos + cart.facing_forward) % len(track)]
    assert pos != npos

    if len(track_ids[npos]) > 1:
        if cart.turn_state:  # left/right turn => switch tracks
            new_track_id = next(t for t in track_ids[npos] if t != track_id)
            new_track = tracks[new_track_id]
            new_track_pos = new_track.index(npos)

            # get original facing dir, then new facing dir
            r1, c1 = pos
            r2, c2 = npos
            dr = (r2 > r1) - (r2 < r1)
            dc = (c2 > c1) - (c2 < c1)

            facing_dir = DIRS4.index((dr, dc))
            idx = (facing_dir + cart.turn_state) % 4
            ndr, ndc = DIRS4[idx]
            npos2 = (r2 + ndr, c2 + ndc)

            i = new_track.index(npos)
            j = new_track.index(npos2)

            cart.track_id = new_track_id
            cart.track_pos = new_track_pos
            cart.facing_forward = 1 if ((i + 1) % len(new_track) == j) else -1
            cart.turn_state = (cart.turn_state + 2) % 3 - 1

            assert ((i + 1) % len(new_track) == j) or ((j + 1) % len(new_track) == i)
        else:
            cart.turn_state = (cart.turn_state + 2) % 3 - 1
            cart.track_pos = (cart.track_pos + cart.facing_forward) % len(track)
    else:
        cart.track_pos = (cart.track_pos + cart.facing_forward) % len(track)


def step_carts():

    for cart in sorted(carts, key=cart_coords):
        if cart not in carts:
            continue

        step_cart(cart)

        # identify and remove crashes
        carts_on_tile = [c for c in carts if cart_coords(c) == cart_coords(cart)]
        if len(carts_on_tile) > 1:
            for c in carts_on_tile:
                carts.remove(c)
                CRASHES.append(c)


def part1():
    print_grid()
    while len(carts) > 1:
        step_carts()
        print_grid()

    r, c = cart_coords(CRASHES[0])
    return f'{c},{r}'


def part2():
    assert len(carts) == 1
    r, c = cart_coords(carts[0])
    return f'{c},{r}'


lines = sys.stdin.read().split('\n')
grid = {(r, c): ch for r, line in enumerate(lines) for c, ch in enumerate(line)}

ul_corners = {
    (r, c)
    for (r, c), v in grid.items()
    if v == '/' and grid.get((r, c + 1), 'X') in '-+><'
}

tracks = []
track_ids = defaultdict(list)  # (r,c) => [...track_ids]
carts: list[Cart] = []
CRASHES = []


def setup():
    for track_id, src in enumerate(ul_corners):
        funcs = [find_right, find_down, find_left, find_up]
        dir_chars = '>v<^'
        track = []

        for next_corner, dir_char in zip(funcs, dir_chars):
            tar = next_corner(*src)
            segment = points_between(src, tar)

            for p in segment:
                track_ids[p].append(track_id)
                if (cart_char := grid[p]) in dir_chars:
                    facing_forward = [-1, 1][cart_char == dir_char]
                    track_position = len(track) + segment.index(p)
                    carts.append(Cart(track_id, track_position, facing_forward, -1))

            track += segment
            src = tar

        tracks.append(track)


setup()

if '-v' not in sys.argv:
    print_grid = lambda: None

print('part1:', a1 := part1())
print('part2:', a2 := part2())

assert a1 == '136,36'
assert a2 == '53,111'
