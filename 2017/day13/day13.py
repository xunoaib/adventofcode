import sys

lines = sys.stdin.read().strip().split('\n')

ranges: dict[int, int] = dict(tuple(map(int, l.split(': '))) for l in lines)


def severity(delay: int):
    sev = 0
    caught = False

    for d in range(max(ranges) + 1):
        if r := ranges.get(d):
            if (d + delay) % (2 * r - 2) == 0:
                sev += d * r
                caught = True

    return sev if caught else None


a1 = severity(0)

delay = 0
while (sev := severity(delay)) is not None:
    delay += 1

print('part1:', a1)
print('part2:', delay)

assert a1 == 1728
assert a2 == 3946838
