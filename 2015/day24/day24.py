import math
import sys

from z3 import If, Int, Or, Solver, sat

ws = list(map(int, sys.stdin))


def make_qe_expr(gwts):
    return math.prod([If(gw == 1, w, 1) for w, gw in zip(ws, gwts)])


def solve(ngroups=3, max_qe=None):
    target_group_weight = sum(ws) // ngroups

    gwtss = [
        [Int(f'gwts{g}_{i}') for i in range(len(ws))] for g in range(ngroups)
    ]

    npkgs = [sum(gwts) for gwts in gwtss]

    s = Solver()

    for gwts in gwtss:
        for gw in gwts:
            s.add(Or(gw == 0, gw == 1))
        s.add(sum(w * gw for w, gw in zip(ws, gwts)) == target_group_weight)

    for vs in zip(*gwtss):
        s.add(sum(vs) == 1)

    for npkg in npkgs[1:]:
        s.add(npkgs[0] < npkg)

    qe = make_qe_expr(gwtss[0])
    min_qe = float('inf')

    if max_qe:
        s.add(qe <= max_qe)

    while s.check() == sat:
        m = s.model()
        s.add(Or([z() != m[z] for z in m]))
        min_qe = m.eval(qe)
        s.add(qe < min_qe)
        print('new min:', min_qe)

    return min_qe.as_long()


a1 = solve(3)
print('part1:', a1)

a2 = solve(4)
print('part2:', a2)

assert a1 == 11846773891
assert a2 == 80393059
