import sys

lines = sys.stdin.read().strip().split('\n')

ranges: dict[int, int] = dict(tuple(map(int, l.split(': '))) for l in lines)


def part1(delay: int):

    sev = 0
    for d in range(max(ranges) + 1):
        d += delay
        if r := ranges.get(d):
            pos = d % (2 * r - 2)
            if pos == 0:
                sev += d * r
    return sev


a1 = part1(0)

print('part1:', a1)

assert a1 == 1728
