import sys
from dataclasses import dataclass, field

sys.setrecursionlimit(10000)


@dataclass
class Node:
    children: list['Node'] = field(default_factory=list)
    metadata: list[int] = field(default_factory=list)


def parse():
    n_children = vs.pop(0)
    n_metadata = vs.pop(0)

    children = [parse() for _ in range(n_children)]
    metadata = [vs.pop(0) for _ in range(n_metadata)]

    return Node(children, metadata)


def metadata_sum(node: Node):
    return sum(node.metadata) + sum(map(metadata_sum, node.children))


def node_value(node: Node):
    if not node.children:
        return sum(node.metadata)

    return sum(
        node_value(node.children[mv - 1]) for mv in node.metadata
        if mv - 1 < len(node.children)
    )


vs = list(map(int, input().split()))

root = parse()
a1 = metadata_sum(root)
a2 = node_value(root)

print('part1:', a1)
print('part2:', a2)

assert a1 == 36627
assert a2 == 16695
