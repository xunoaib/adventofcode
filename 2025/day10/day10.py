import sys

from z3 import Int, Optimize, sat

lines = sys.stdin.read().strip().split('\n')


def neighbors(buttons, state):
    for bs in buttons:
        s = list(state)
        for b in bs:
            s[b] = not s[b]
        yield tuple(s)


class Machine:

    def __init__(self, line):
        lights, *buttons, req = [g[1:-1] for g in line.split(' ')]
        self.buttons = tuple(tuple(map(int, g.split(','))) for g in buttons)
        self.goal_lights = tuple(ch == '#' for ch in lights)
        self.goal_jolts = tuple(map(int, req.split(',')))


def solve_part1(buttons, goal):
    q = [(0, (False, ) * len(goal))]
    seen = {q[0][1]}
    while q:
        cost, lights = q.pop(0)
        if lights == goal:
            return cost
        for n in neighbors(buttons, lights):
            if n not in seen:
                seen.add(n)
                q.append((cost + 1, n))
    assert False


def solve_part2(buttons, goal):
    presses = [Int(f'presses{i}') for i in range(len(buttons))]

    s = Optimize()
    for p in presses:
        s.add(p >= 0)

    output_accs = {i: 0 for i in range(len(goal))}

    for p, bs in zip(presses, buttons):
        for b in bs:
            output_accs[b] += p

    for i in range(len(goal)):
        s.add(output_accs[i] == goal[i])

    s.minimize(sum(presses))

    assert s.check() == sat

    m = s.model()
    return sum(m[p].as_long() for p in presses)


a1 = a2 = 0
for line in lines:
    m = Machine(line)
    a1 += solve_part1(m.buttons, m.goal_lights)
    a2 += solve_part2(m.buttons, m.goal_jolts)

print('part1:', a1)
print('part2:', a2)

assert a1 == 571
assert a2 == 20869
