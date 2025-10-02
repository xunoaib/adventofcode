import math
import sys

from z3 import And, If, Int, Optimize, Or, Solver, sat

ws = list(map(int, sys.stdin))


def part1():
    target_group_weight = sum(ws) // 3

    gwts1 = [Int(f'gwts1_{i}') for i in range(len(ws))]
    gwts2 = [Int(f'gwts2_{i}') for i in range(len(ws))]
    gwts3 = [Int(f'gwts3_{i}') for i in range(len(ws))]
    gwtss = [gwts1, gwts2, gwts3]

    s = Solver()
    # s = Optimize()

    for gwts in [gwts1, gwts2, gwts3]:
        for gw in gwts:
            s.add(Or(gw == 0, gw == 1))
        s.add(sum(w * gw for w, gw in zip(ws, gwts)) == target_group_weight)

    for v1, v2, v3 in zip(gwts1, gwts2, gwts3):
        s.add(v1 + v2 + v3 == 1)

    npkgs = [sum(gwts) for gwts in gwtss]
    s.add(npkgs[0] < npkgs[1])
    s.add(npkgs[0] < npkgs[2])

    def make_qe_expr(gwts):
        return math.prod([If(gw == 1, w, 1) for w, gw in zip(ws, gwts)])

    def create_groups(m):
        return [
            [w for w, gw in zip(ws, gwts) if m.eval(gw) == 1] for gwts in gwtss
        ]

    # s.minimize(qe_expr(gwts1))

    min_qe = float('inf')
    qe = make_qe_expr(gwts1)
    s.add(qe <= 11846773891)

    while s.check() == sat:
        m = s.model()
        s.add(Or([z() != m[z] for z in m]))

        min_qe = m.eval(qe)
        s.add(qe < min_qe)

        print(min_qe, create_groups(m))

    return min_qe


a1 = part1()
print('part1:', a1)
