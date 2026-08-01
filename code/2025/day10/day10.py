from z3 import And, Int, Optimize, sat


def solve_part1(buttons, goals):
    q = [(0, (False, ) * len(goals))]
    seen = {q[0][1]}

    while q:
        cost, lights = q.pop(0)
        if lights == goals:
            return cost

        for n in neighbors(buttons, lights):
            if n not in seen:
                seen.add(n)
                q.append((cost + 1, n))


def solve_part2(buttons, goals):
    presses = [Int(f'p{i}') for i in range(len(buttons))]
    totals = [0] * len(goals)

    s = Optimize()
    s.add(And(p >= 0 for p in presses))

    for p, bs in zip(presses, buttons):
        for b in bs:
            totals[b] += p

    s.add(And(t == g for t, g in zip(totals, goals)))
    s.minimize(sum(presses))

    assert s.check() == sat
    m = s.model()
    return m.evaluate(sum(presses)).as_long()


def neighbors(buttons, state):
    for bs in buttons:
        yield tuple(v ^ (i in bs) for i, v in enumerate(state))


def parse(line):
    lights, *buttons, req = [g[1:-1] for g in line.split(' ')]
    buttons = tuple(tuple(map(int, g.split(','))) for g in buttons)
    lights = tuple(ch == '#' for ch in lights)
    jolts = tuple(map(int, req.split(',')))
    return buttons, lights, jolts


a1 = a2 = 0

for line in open(0):
    buttons, lights, jolts = parse(line.strip())
    a1 += solve_part1(buttons, lights)
    a2 += solve_part2(buttons, jolts)

print('part1:', a1)
print('part2:', a2)

assert a1 == 571
assert a2 == 20869
