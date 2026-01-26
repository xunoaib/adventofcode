def is_open(x, y):
    if x < 0 or y < 0:
        return False
    v = N + x * x + 3 * x + 2 * x * y + y + y * y
    return f'{v:b}'.count('1') % 2 == 0


def neighbors4(r, c):
    return {(r + dr, c + dc) for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]}


def part1(src, tar):
    q = [(0, src)]
    seen = {src}
    while q:
        cost, p = q.pop(0)
        if p == tar:
            return cost
        for n in neighbors4(*p):
            if n not in seen and is_open(*n):
                q.append((cost + 1, n))
                seen.add(n)


def part2(src, steps):
    assert is_open(*src)
    q = [(0, src)]
    seen = {src: 0}
    while q:
        cost, p = q.pop(0)
        if cost > steps:
            break
        for n in neighbors4(*p):
            if n not in seen and is_open(*n):
                q.append((cost + 1, n))
                seen[n] = cost + 1

    return sum(d <= steps for d in seen.values())


N = int(input())

src = (1, 1)
tar = (31, 39)

a1 = part1(src, tar)
a2 = part2(src, 50)

print('part1:', a1)
print('part2:', a2)

assert a1 == 90
assert a2 == 135
