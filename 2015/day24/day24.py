import sys

from z3 import And, Int, Optimize, Or, Solver, sat

ws = list(map(int, sys.stdin))

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
# for gwts in gwtss:
#     s.add(sum(gwts) ==)

# s.minimize(npkgs[0])
s.add(npkgs[0] < npkgs[1])
s.add(npkgs[0] < npkgs[2])


def create_groups(m):
    return [
        [w for w, gw in zip(ws, gwts) if m.eval(gw) == 1] for gwts in gwtss
    ]


while s.check() == sat:
    m = s.model()

    s.add(Or([z() != m[z] for z in m]))
    sels = tuple(tuple(m[gw].as_long() for gw in gwts) for gwts in gwtss)
    # print(hash(sels))

    # print([m.eval(np) for np in npkgs])

    print(create_groups(m))

    # sel1 = [m[gw].as_long() for gw in gwts1]
    # sel2 = [m[gw].as_long() for gw in gwts2]
    # sel3 = [m[gw].as_long() for gw in gwts3]
    #
    # print(sel1)
    # print(sel2)
    # print(sel3)
