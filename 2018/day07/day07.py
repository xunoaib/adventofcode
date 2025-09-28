import sys
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass


class Worker:

    def __init__(self):
        self.node = ''
        self.timeleft = 0

    def tick(self):
        self.timeleft -= 1
        return self.timeleft == 0

    def assign(self, node: str, timeleft: int):
        self.node = node
        self.timeleft = timeleft

    @property
    def completed(self):
        return self.timeleft <= 0


class WorkerPool:

    def __init__(self, num_workers: int, base_time: int):
        self.workers = [Worker() for _ in range(num_workers)]
        self.base_time = base_time

    def assign(self, nodes: list[str]):
        nodes = list(nodes)
        for w in self.workers:
            if nodes and w.completed:
                n = nodes.pop(0)
                w.assign(n, self.base_time + ord(n) - ord('A') + 1)

    def tick(self):
        return [w.node for w in self.workers if w.tick()]

    @property
    def working_nodes(self):
        return [w.node for w in self.workers if not w.completed]


def find_candidates(deps: dict[str, set[str]], skip: list[str] = []):
    return sorted(
        node for node, nodes in deps.items() if not nodes and node not in skip
    )


def part1(deps):
    s = ''
    while deps:
        c = find_candidates(deps)[0]
        s += c
        remove_node(deps, c)
    return s


def part2(deps: dict[str, set[str]]):
    # pool = WorkerPool(2, 0)  # Sample input
    pool = WorkerPool(5, 60)  # Real input

    ticks = 0
    while deps:
        pool.assign(find_candidates(deps, pool.working_nodes))
        if completed := pool.tick():
            remove_nodes(deps, completed)
        ticks += 1

    return ticks


def remove_nodes(deps: dict[str, set[str]], nodes: list[str]):
    for n in nodes:
        remove_node(deps, n)


def remove_node(deps: dict[str, set[str]], node: str):
    del deps[node]
    for v in deps.values():
        v.discard(node)


def main():
    deps: dict[str, set[str]] = defaultdict(set)

    for line in sys.stdin:
        args = line.split()
        a, b = args[1], args[-3]
        deps[a]
        deps[b].add(a)

    a1 = part1(deepcopy(deps))
    a2 = part2(deepcopy(deps))

    print('part1:', a1)
    print('part2:', a2)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
