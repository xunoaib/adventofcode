#!/usr/bin/env python3
import re
import sys


class Node:

    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.children = {}

    def get_size(self):
        return self.size + sum(c.get_size() for n, c in self.children.items())

    def add_child(self, name, size=0):
        if name not in self.children:
            self.children[name] = Node(name, size)
        elif size != 0:
            self.children[name].size = size
        return self.children[name]

    def find_dirs_lt(self, size):
        """ Find dirs with a total size less than or equal to `size` """
        dirs = []
        for d in self.children.values():
            if d.size == 0 and d.get_size() <= size:
                dirs.append(d)
            dirs += d.find_dirs_lt(size)
        return dirs

    def find_dirs_gt(self, size):
        """ Find dirs with a total size greater than or equal to `size` """
        # note: this wont return the root dir, but that didnt matter
        dirs = []
        for d in self.children.values():
            if d.size == 0 and d.get_size() >= size:
                dirs.append(d)
            dirs += d.find_dirs_gt(size)
        return dirs

    def __repr__(self):
        ftype = 'file' if self.size else 'dir'
        return f'{self.name} ({ftype}, size={self.get_size()})'


def main():
    lines = sys.stdin.read().strip().split('\n')

    root = Node('/')
    dirs = [root]

    for line in lines:
        if m := re.match(r'\$ cd (.*)', line):
            name = m.group(1)
            if name == '..':
                dirs.pop()
            elif name != '/':
                child = dirs[-1].add_child(name)
                dirs.append(child)
        elif line == '$ ls':
            pass
        elif m := re.match(r'dir (.*)', line):
            name = m.group(1)
            dirs[-1].add_child(name)
        elif m := re.match(r'(.*) (.*)', line):
            size, name = m.groups()
            dirs[-1].add_child(name, int(size))

    dirs1 = root.find_dirs_lt(100000)
    part1 = sum(d.get_size() for d in dirs1)
    print('part1:', part1)

    freespace = 70000000 - root.get_size()
    minneeded = 30000000 - freespace

    dirs2 = root.find_dirs_gt(minneeded)
    sizes = [d.get_size() for d in dirs2]
    part2 = min(sizes)
    print('part2:', part2)

    assert part1 == 1644735
    assert part2 == 1300850


if __name__ == '__main__':
    main()
