import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field


@dataclass
class Disc:
    id: str
    weight: int
    above: list['Disc'] = field(default_factory=list)

    @property
    def total_weight(self):
        return self.weight + self.weight_above

    @property
    def weight_above(self):
        return sum(d.total_weight for d in self.above)


def parse_input(data: str):
    lines = data.splitlines()

    weights: dict[str, int] = {}
    holding: dict[str, set[str]] = defaultdict(set)
    depends_on = defaultdict(set)

    for line in lines:
        if m := re.match(r'^(.*?) \((.*)\) -> (.*)$', line):
            l = m.group(1)
            rs = m.group(3).split(', ')
            holding[l]
            for r in rs:
                holding[r].add(l)
            weights[l] = int(m.group(2))
        elif m := re.search(r'^(.*?) \((.*)\)', line):
            l = m.group(1)
            holding[l]
            weights[l] = int(m.group(2))

    return weights, dict(holding)


def walk_anomaly_tree(discs: dict[str, Disc], node):
    hist = []
    while True:
        above = discs[node].above
        ws = [d.total_weight for d in above]
        counts = Counter(ws)
        unique = [d for d in above if counts[d.total_weight] == 1]
        expected = [d for d in above if counts[d.total_weight] > 1]

        print()
        print('above:  ', [d.id for d in above])
        print('weights:', ws)
        # print(uniques)

        if len(unique) != 1:
            break

        w_e = expected[0].total_weight
        w_u = unique[0].total_weight
        hist.append((w_e, w_u, expected[0].id, unique[0].id, w_e - w_u))
        node = unique[0].id

    return hist


def main():
    weights, holding = parse_input(sys.stdin.read())
    assert len(weights) == len(holding)

    a1 = next(k for k, v in holding.items() if not v)
    print('part1:', a1)

    discs = {n: Disc(n, w) for n, w in weights.items()}

    for r, ls in holding.items():
        for l in ls:
            discs[l].above.append(discs[r])

    hist = walk_anomaly_tree(discs, a1)

    we, wu, eid, uid, diff = hist[-1]
    a2 = discs[uid].weight + diff

    print('part2:', a2)

    assert a2 == 362


if __name__ == '__main__':
    main()
