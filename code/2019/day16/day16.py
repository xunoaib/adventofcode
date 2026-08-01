from itertools import cycle, product


def pattern(length: int):
    assert length > 0
    base = [v for v in (0, 1, 0, -1) for _ in range(length)]
    it = cycle(base)
    next(it)
    yield from it


def next_list(s: list[int]):
    result = []
    for i, _ in enumerate(s):
        t = [sv * pv for sv, pv in zip(s, pattern(i + 1))]
        result.append(abs(sum(t)) % 10)
    return result


s = list(map(int, input()))

for _ in range(100):
    s = next_list(s)

a1 = ''.join(str(v) for v in s[:8])
print('part1:', a1)
