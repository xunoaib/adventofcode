from functools import cache


def part1(cur):
    return 1 if cur == 'out' else sum(map(part1, g[cur]))


@cache
def part2(cur, s=0):
    return s == 3 if cur == 'out' else sum(
        part2(n, s | (n == 'fft') | (n == 'dac') * 2) for n in g[cur]
    )


g = {a[:-1]: b for a, *b in map(str.split, open(0))}

a1 = part1('you')
a2 = part2('svr')

print('part1:', a1)
print('part2:', a2)

assert a1 == 674
assert a2 == 438314708837664
