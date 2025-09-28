import sys
from collections import defaultdict
from dataclasses import dataclass


class Worker:

    def __init__(self, id: int):
        self.id = id
        self.node = ''
        self.timeleft = 0

    def tick(self):
        if self.timeleft == 0:
            return False

        self.timeleft -= 1

        if self.timeleft == 0:
            print(f'Worker {self.id} finished {self.node}')
            return True

        return False

    def assign(self, node: str, timeleft: int):
        self.node = node
        self.timeleft = timeleft

    @property
    def completed(self):
        return self.timeleft == 0


class WorkerPool:

    def __init__(self, num_workers: int, base_time: int):
        self.workers = [Worker(i) for i in range(num_workers)]
        self.base_time = base_time

    def assign(self, nodes: list[str]):
        nodes = list(nodes)
        for w in self.workers:
            if nodes and w.completed:
                n = nodes.pop(0)
                print(f'Assigning {n} to Worker {w.id}')
                w.assign(n, self.base_time + ord(n) - ord('A') + 1)

    def tick(self):
        return [w.node for w in self.workers if w.tick()]

    def active_nodes(self):
        return [w.node for w in self.workers if not w.completed]


def find_candidates(deps: dict[str, set[str]], ignore: list[str] = []):
    return sorted(k for k, v in deps.items() if not v and k not in ignore)


def part1(deps):
    s = ''
    while deps:
        c = find_candidates(deps)[0]
        s += c

        del deps[c]
        for k, v in deps.items():
            v.discard(c)
    return s


def part2(deps: dict[str, set[str]]):
    # pool = WorkerPool(2, 0)
    pool = WorkerPool(5, 60)

    free = find_candidates(deps)
    pool.assign(free)

    ticks = 0
    while deps:
        if completed := pool.tick():
            print('Completed', completed)
            remove_nodes(deps, completed)
            pool.assign(find_candidates(deps, pool.active_nodes()))
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

    a1 = part1(dict(deps))
    a2 = part2(dict(deps))

    print('part1:', a1)
    print('part2:', a2)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
