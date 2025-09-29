N, E, S, W = range(4)

OFFSETS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def part1(commands: list[str]):
    d = r = c = 0

    for cmd in commands:
        t, v = cmd[0], int(cmd[1:])
        d += 1 if t == 'R' else -1
        d %= 4
        r += v * OFFSETS[d][0]
        c += v * OFFSETS[d][1]

    return abs(r) + abs(c)


def part2(commands: list[str]):
    d = r = c = 0

    visited = {(r, c)}
    for cmd in commands:
        t, v = cmd[0], int(cmd[1:])
        d += 1 if t == 'R' else -1
        d %= 4
        for _ in range(v):
            r += OFFSETS[d][0]
            c += OFFSETS[d][1]
            if (r, c) in visited:
                return abs(r) + abs(c)
            visited.add((r, c))


def main():
    commands = input().split(', ')

    a1 = part1(commands)
    a2 = part2(commands)

    print('part1:', a1)
    print('part2:', a2)


if __name__ == '__main__':
    main()
