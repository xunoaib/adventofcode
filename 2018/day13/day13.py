import sys
from collections import defaultdict
from dataclasses import dataclass

DIRS4 = R, D, L, U = (0, 1), (1, 0), (0, -1), (-1, 0)

FACING_R, FACING_D, FACING_L, FACING_U = range(4)


@dataclass
class Cart:
    track_id: int
    track_pos: int  # position on track
    facing_forward: int  # direction on track (1=forward, -1=backward)
    turn_state: int  # next turn ID (-1, 0, 1)


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
    facing_dir: int,
    track: list[tuple[int, int]],
):
    i = track.index(pos)

    forward_dirs = {
        (0, FACING_U),
        (0, FACING_R),
        (4, FACING_R),
        (4, FACING_D),
        (8, FACING_D),
        (8, FACING_L),
        (12, FACING_L),
        (12, FACING_U),
    }
    if i % 4 == 0:
        return 1 if (i, facing_dir) in forward_dirs else -1

    section = i // (len(track) // 4)

    print('#', pos, facing_dir, i, section)

    return {
        (0, FACING_R): 1,
        (0, FACING_L): -1,
        (1, FACING_D): 1,
        (1, FACING_U): -1,
        (2, FACING_R): -1,
        (2, FACING_L): 1,
        (3, FACING_D): -1,
        (3, FACING_U): 1,
    }[section, facing_dir]


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
carts: list[Cart] = []

tile_track_ids = defaultdict(list)

for track_id, src in enumerate(ul_corners):
    funcs = [find_right, find_down, find_left, find_up]
    dir_chars = '>v<^'
    points = []

    for next_corner, dir_char in zip(funcs, dir_chars):
        tar = next_corner(*src)
        segment = points_between(src, tar)

        for p in segment:
            tile_track_ids[p].append(track_id)
            if (cart_char := grid[p]) in dir_chars:
                facing_forward = 1 if cart_char == dir_char else -1
                track_position = len(points) + segment.index(p)
                carts.append(Cart(track_id, track_position, facing_forward, -1))

        points += segment
        src = tar

    tracks.append(points)


def step_carts():
    print('\n === STEP ===\n')

    for cart in carts:
        track_id = cart.track_id
        track = tracks[track_id]

        pos = track[cart.track_pos]
        npos = track[(cart.track_pos + cart.facing_forward) % len(track)]

        assert pos != npos

        if grid[npos] == '+':
            print('--- intersection')
            if cart.turn_state:  # left/right turn => switch tracks
                new_track_id = next(t for t in tile_track_ids[npos] if t != track_id)
                new_track_pos = tracks[new_track_id].index(npos)
                new_track = tracks[new_track_id]

                # get original facing dir, then new facing dir
                r1, c1 = pos
                r2, c2 = npos
                dr = (r2 > r1) - (r2 < r1)
                dc = (c2 > c1) - (c2 < c1)

                facing_dir = DIRS4.index((dr, dc))
                new_facing_dir = ndr, ndc = DIRS4[(facing_dir + cart.turn_state) % 4]
                npos2 = (r2 + ndr, c2 + ndc)

                i = new_track.index(npos)
                j = new_track.index(npos2)

                # print(i, j, len(track), len(new_track))

                cart.track_id = new_track_id
                cart.track_pos = new_track_pos
                cart.facing_forward = 1 if ((i + 1) % len(new_track) == j) else -1

                assert ((i + 1) % len(new_track) == j) or (
                    (j + 1) % len(new_track) == i
                )

            cart.turn_state = (cart.turn_state + 2) % 3 - 1
        else:
            print('--- no intersection')
            cart.track_pos = (cart.track_pos + 1) % len(track)

        # track_dir = get_track_dir(npos, facing_dir, tracks[track_id])
        # print('track_dir:', track_dir)


# __import__('pprint').pprint(dict(sorted(track_facing_dir.items())))
# exit()

for _ in range(100):
    step_carts()
    print(carts)


if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
