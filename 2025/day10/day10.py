import sys

from z3 import Int, Optimize, sat

lines = sys.stdin.read().strip().split('\n')


class Machine:

    def __init__(self, line):
        lights, *buttons, req = [g[1:-1] for g in line.split(' ')]
        self.goal = tuple(ch == '#' for ch in lights)
        self.buttons = tuple(tuple(map(int, g.split(','))) for g in buttons)
        self.state = (False, ) * len(self.goal)
        self.goal_jolts = tuple(map(int, req.split(',')))

    def neighbors(self, state):
        for bs in self.buttons:
            s = list(state)
            for b in bs:
                s[b] = not s[b]
            yield tuple(s)

    def solve_part1(self):
        q = [(0, self.state)]
        seen = {self.state}
        while q:
            cost, s = q.pop(0)
            if s == self.goal:
                return cost

            for n in self.neighbors(s):
                if n not in seen:
                    seen.add(n)
                    q.append((cost + 1, n))

        assert False

    def solve_part2(self):
        n = len(self.buttons)
        nj = len(self.goal_jolts)
        presses = [Int(f'presses{i}') for i in range(n)]
        outputs = [Int(f'o{i}') for i in range(nj)]

        s = Optimize()
        for p in presses:
            s.add(p >= 0)

        output_accs = {i: 0 for i in range(nj)}

        for bidx, bs in enumerate(self.buttons):
            for b in bs:
                output_accs[b] += presses[bidx]

        for i, o in enumerate(outputs):
            s.add(o == self.goal_jolts[i])
            s.add(o == output_accs[i])

        s.minimize(sum(presses))

        assert s.check() == sat

        m = s.model()
        return sum(m[p].as_long() for p in presses)


a1 = a2 = 0
for line in lines:
    m = Machine(line)
    a1 += m.solve_part1()
    a2 += m.solve_part2()

print('part1:', a1)
print('part2:', a2)

assert a1 == 571
assert a2 == 20869
