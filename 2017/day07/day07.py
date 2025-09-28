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


def part2(discs: dict[str, Disc], node):
    expected_weight = None

    while True:
        above = discs[node].above
        counts = Counter(d.total_weight for d in above)
        anomaly = next((d for d in above if counts[d.total_weight] == 1), None)
        normal = next((d for d in above if counts[d.total_weight] > 1), None)

        if normal is None or anomaly is None:
            break

        expected_weight = anomaly.weight + normal.total_weight - anomaly.total_weight
        node = anomaly.id

    return expected_weight


def main():
    weights, holding = parse_input(sys.stdin.read())

    a1 = next(k for k, v in holding.items() if not v)

    discs = {n: Disc(n, w) for n, w in weights.items()}
    for r, ls in holding.items():
        for l in ls:
            discs[l].above.append(discs[r])

    a2 = part2(discs, a1)

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 'vvsvez'
    assert a2 == 362


if __name__ == '__main__':
    main()
