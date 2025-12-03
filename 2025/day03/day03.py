import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import combinations, pairwise, permutations, product

aa = bb = None

lines = sys.stdin.read().strip().split('\n')

aa = bb = 0

for line in lines:
    xs = list(map(int, list(line)))

    m = 0
    for a, b in combinations(xs, r=2):
        m = max(m, int(f'{a}{b}'))

    aa += m

for line in lines:
    xs = list(map(int, list(line)))

    vals = [(v, i) for i, v in enumerate(xs)]
    vals.sort(key=lambda vi: (-vi[0], vi[1]))
    left = 12

    print()
    print('>>> Line', line)
    print()

    s = []
    cur_idx = None
    while left:
        # if not vals:
        #     s += xs[idx:idx + left]
        #     break

        for v, i in vals:
            print(vals)
            if i <= len(xs) - left:
                print(f'popping {v} @ {i}')
                left -= 1
                cur_idx = i
                s.append(v)
                vals = [(vv, ii) for vv, ii in vals if ii > cur_idx]
                break
        else:
            print('nothing found', s, vals)
            exit()

    s = ''.join(map(str, s))
    print(s)
    bb += int(s)

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 17301
assert bb == 3121910778619
