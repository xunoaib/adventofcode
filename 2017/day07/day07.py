import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Disc:
    id: str
    weight: int
    above: list['Disc'] = field(default_factory=list)

    # @property
    # def total_weight(self):
    #     return self.weight + self.weight_above

    # @property
    # def weight_above(self):
    #     return sum(d.total_weight for d in self.above)


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


def main():
    weights, holding = parse_input(sys.stdin.read())
    assert len(weights) == len(holding)

    a1 = next(k for k, v in holding.items() if not v)
    print('part1:', a1)

    discs = {n: Disc(n, w) for n, w in weights.items()}

    for r, ls in holding.items():
        for l in ls:
            discs[l].above.append(discs[r])

    print([x.id for x in discs[a1].above])


if __name__ == '__main__':
    main()
