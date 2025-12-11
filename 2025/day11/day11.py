import sys
from collections import defaultdict
from functools import cache


def part1(cur):
    return 1 if cur == 'out' else sum(part1(n) for n in g[cur])


@cache
def part2(cur, s: int = 0):
    return s == 3 if cur == 'out' else sum(
        part2(n, s | 1 * (n == 'fft') | 2 * (n == 'dac')) for n in g[cur]
    )


lines = sys.stdin.read().strip().split('\n')

g = defaultdict(set)
for line in lines:
    a, *bs = line.split(' ')
    g[a[:-1]] |= set(bs)

a1 = part1('you')
a2 = part2('svr')

print('part1:', a1)
print('part2:', a2)

assert a1 == 674
assert a2 == 438314708837664
