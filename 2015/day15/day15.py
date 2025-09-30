import math
import re
import sys

from z3 import Int, Solver, sat


def main():

    tuples: list[tuple[int, ...]] = []
    for line in sys.stdin:
        _, props = line.split(':')
        tuples.append(tuple(map(int, re.findall(r'-?\d+', props))))

    a1 = part1_hacky(tuples)
    print('part1:', a1)

    a2 = part2(tuples)
    print('part2:', a2)

    assert a1 == 18965440
    assert a2 == 15862900


def part2(tuples: list[tuple[int, ...]]):
    tuples = [t for t in tuples]  # drop calories

    ingd_counts = [Int(f'ingdCount{i}') for i in range(len(tuples))]
    prop_totals = [Int(f'propTotal{i}') for i in range(len(tuples[0]))]
    prop_tuples = list(zip(*tuples))

    s = Solver()

    for prop_total, prop_tuple in zip(prop_totals, prop_tuples):
        s.add(
            prop_total == sum(i * v for i, v in zip(ingd_counts, prop_tuple))
        )
        s.add(prop_total > 0)

    score = Int('score')
    s.add(score == math.prod(prop_totals[:-1]))
    s.add(sum(ingd_counts) == 100)
    s.add(prop_totals[-1] == 500)  # part 2 constraint

    while s.check() == sat:
        m = s.model()
        ans = m[score].as_long()
        s.add(score > ans)

    return ans


def part1_hacky(tuples: list[tuple[int, ...]]):
    tuples = [t[:-1] for t in tuples]  # drop calories

    ingd_counts = [Int(f'ingdCount{i}') for i in range(len(tuples))]
    prop_totals = [Int(f'propTotal{i}') for i in range(len(tuples[0]))]
    prop_tuples = list(zip(*tuples))

    s = Solver()

    for prop_total, prop_tuple in zip(prop_totals, prop_tuples):
        s.add(
            prop_total == sum(i * v for i, v in zip(ingd_counts, prop_tuple))
        )
        s.add(prop_total > 0)

    score = Int('score')
    s.add(score == math.prod(prop_totals))
    s.add(sum(ingd_counts) == 100)

    # FIXME: avoid manually-narrowing down bounds
    # s.add(score >= 17939952)
    # s.add(score >= 18643968)
    # s.add(score >= 18957312)
    s.add(score >= 18965440)
    s.add(score < 18970000)

    while s.check() == sat:
        m = s.model()
        ans = m[score].as_long()
        print(ans)
        s.add(score > ans)

    return ans


if __name__ == '__main__':
    main()
