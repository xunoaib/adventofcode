#!/usr/bin/env python3
import copy
import math
import re
import sys
from itertools import permutations


class Literal:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent

    def __repr__(self):
        return f'{self.value}'

    def __iadd__(self, value):
        if isinstance(value, Literal):
            value = value.value
        self.value += value

    def magnitude(self):
        return self.value


class Pair:
    def __init__(self, left, right, parent=None):
        self.parent = parent
        self.left = left
        self.right = right

        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self

    def __add__(self, other):
        return Pair(copy.deepcopy(self), copy.deepcopy(other))

    def __repr__(self):
        return f'[{self.left},{self.right}]'

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    @staticmethod
    def fromlist(items, parent=None):
        if isinstance(items, int):
            return Literal(items, parent)
        left, right = map(Pair.fromlist, items)
        return Pair(left, right, parent)

    def left_sibling(self):
        node = self
        while node.parent.left == node:
            node = node.parent
            if node.parent is None:
                return None

        node = node.parent.left
        while not isinstance(node, Literal):
            node = node.right
        return node

    def right_sibling(self):
        node = self
        while node.parent.right == node:
            node = node.parent
            if node.parent is None:
                return None

        node = node.parent.right
        while not isinstance(node, Literal):
            node = node.left
        return node

    def replace(self, old_node, new_node):
        if self.left == old_node:
            self.left = new_node
            self.left.parent = self
        elif self.right == old_node:
            self.right = new_node
            self.right.parent = self

    def explode(self, depth=0):
        if depth >= 4:
            if left := self.left_sibling():
                left += self.left
            if right := self.right_sibling():
                right += self.right
            self.parent.replace(self, Literal(0))
            return True

        for pair in (self.left, self.right):
            if isinstance(pair, Pair):
                if pair.explode(depth + 1):
                    return True
        return False

    def split(self, depth=0):
        for node in (self.left, self.right):
            if isinstance(node, Literal) and node.value >= 10:
                left = Literal(math.floor(node.value / 2))
                right = Literal(math.ceil(node.value / 2))
                self.replace(node, Pair(left, right, node.parent))
                return True

            if isinstance(node, Pair) and node.split():
                return True
        return False

    def simplify(self):
        while self.explode() or self.split():
            pass
        return self


def main():
    data = sys.stdin.read().strip()
    if m := re.findall(r'[^\d,\[\]\r\n]', data):
        print(f'untrusted input: {m}')
        return
    pairs = [Pair.fromlist(eval(line)) for line in data.split('\n')]

    pair = pairs[0]
    for other in pairs[1:]:
        pair += other
        pair.simplify()
    ans1 = pair.magnitude()
    print('part1:', ans1)

    best = -sys.maxsize
    for a, b in permutations(pairs, 2):
        if a == b:
            continue
        mag = (a + b).simplify().magnitude()
        if mag > best:
            best = mag

    print('part2:', best)

    assert ans1 == 4184
    assert best == 4731


if __name__ == '__main__':
    main()
