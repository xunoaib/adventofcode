import sys
from dataclasses import dataclass, field

sys.setrecursionlimit(10000)


@dataclass
class Node:
    children: list['Node'] = field(default_factory=list)
    metadata: list[int] = field(default_factory=list)


vs = list(map(int, input().split()))


def parse(i: int):
    print(i)
    n_children = vs[i]
    n_metadata = vs[i + 1]
    i += 2

    children: list[Node] = []
    for _ in range(n_children):
        i, child = parse(i)
        children.append(child)

    metadata = vs[i:i + n_metadata]

    return i, Node(children, metadata)


i, n = parse(0)

print(n)
