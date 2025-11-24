import sys
from dataclasses import dataclass, field

sys.setrecursionlimit(10000)


@dataclass
class Node:
    children: list['Node'] = field(default_factory=list)
    metadata: list[int] = field(default_factory=list)


def parse():
    global tot

    n_children = vs.pop(0)
    n_metadata = vs.pop(0)

    children: list[Node] = []
    for _ in range(n_children):
        children.append(parse())

    metadata = [vs.pop(0) for _ in range(n_metadata)]
    tot += sum(metadata)
    return Node(children, metadata)


vs = list(map(int, input().split()))
vs_orig = list(vs)
tot = 0

n = parse()

print('part1:', tot)
