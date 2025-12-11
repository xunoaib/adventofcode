import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')

g = defaultdict(set)
for line in lines:
    a, *bs = line.split(' ')
    a = a[:-1]
    g[a] |= set(bs)

print(g)

counts = Counter()


def dfs(cur, tar):
    # print(cur)
    if cur == 'out':
        return 1

    t = 0
    for n in g[cur]:
        t += dfs(n, tar)

    return t


aa = dfs('you', 'out')

# q = ['you']
# seen = {q[0]}
# aa = 0
# while q:
#     p, path = q.pop()
#     if p == 'out':
#         aa += 1
#     for n in g[p]:
#         if n not in seen:
#             seen.add(n)
#             q.append(n)

# grid = {
#     (r, c): ch
#     for r, line in enumerate(lines)
#     for c, ch in enumerate(line)
# }

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
