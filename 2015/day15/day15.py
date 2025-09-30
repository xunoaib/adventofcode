import math
import re
import sys

from z3 import Int, Optimize, Solver, sat


def main():

    tuples: list[tuple[int, ...]] = []
    for line in sys.stdin:
        _, props = line.split(':')
        tuples.append(tuple(map(int, re.findall(r'-?\d+', props))))

    # cals = [t[-1] for t in tuples]
    tuples = [t[:-1] for t in tuples]  # drop calories

    ingd_counts = [Int(f'ingdCount{i}') for i in range(len(tuples))]
    prop_totals = [Int(f'propTotal{i}') for i in range(len(tuples[0]))]
    prop_tuples = list(zip(*tuples))

    # s = Optimize()
    s = Solver()

    for prop_total, prop_tuple in zip(prop_totals, prop_tuples):
        s.add(
            prop_total == sum(i * v for i, v in zip(ingd_counts, prop_tuple))
        )
        s.add(prop_total > 0)

    score = Int('score')
    s.add(score == math.prod(prop_totals))
    s.add(sum(ingd_counts) == 100)
    # s.maximize(score)

    # manually-narrow down bounds
    s.add(score > 18960000)
    s.add(score < 18970000)

    # part 2 constraints

    while s.check() == sat:
        m = s.model()
        a1 = m[score].as_long()
        print(a1)
        s.add(score > a1)

    print('part1:', a1)


if __name__ == '__main__':
    main()
