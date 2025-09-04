#!/usr/bin/env python

class Node:
    def __init__(self, value):
        self.value = value
        self.node = None

    def __iter__(self):
        return self

    def __next__(self):
        return self.node

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.value == other.value
        return self.value == other

    def __mul__(self, other):
        if isinstance(other, Node):
            return self.value * other.value
        return self.value * other

    def __gt__(self, other):
        if isinstance(other, Node):
            return self.value > other.value
        return self.value > other

class Puzzle:
    def __init__(self, cups):
        self.cups = {}
        self.maxval = cups[0].value
        self.pointer = cups[0] # currently selected cup

        for i,cup in enumerate(cups):
            cup.node = cups[(i+1) % len(cups)]
            self.cups[cup.value] = cup

            if cup.value > self.maxval:
                self.maxval = cup.value

        cup.node = cups[0] # link tail to head

    def move(self):
        # grab the next 3 cups
        held = []
        node = self.pointer
        for i in range(3):
            held.append(node.node)
            node = node.node

        # unlink after currently selected cup
        self.pointer.node = held[-1].node

        # find destination cup
        destval = self.pointer.value - 1
        while destval in held or destval not in self.cups:
            destval = (destval - 1) % (self.maxval + 1)

        # insert held cups after destination
        destcup = self.cups[destval]
        held[-1].node = destcup.node  # connect held cups after destination
        destcup.node = held[0]  # connect destination to held cups

        # advance to next cup
        self.pointer = self.pointer.node

data = '487912365'
cups = [Node(int(v)) for v in data]

puzzle = Puzzle(cups)
for i in range(100):
    puzzle.move()

print('part1:', end=' ')
cup = puzzle.cups[1]
ans = ''
while cup.node.value != 1:
    cup = cup.node
    ans += str(cup)
print(ans)
assert ans == '89573246'

# part 2
cups += [Node(val) for val in range(max(cups).value+1, 10**6+1)]
puzzle = Puzzle(cups)

for i in range(10**7-100):
    puzzle.move()

cup = puzzle.cups[1]
ans = cup.node * cup.node.node
print('part2:', ans)
assert ans == 2029056128
