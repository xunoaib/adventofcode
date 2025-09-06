import sys
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from itertools import batched, product

POS, IMM, REL = 0, 1, 2

DIRS = [1, 2, 3, 4]
DIR_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Output:

    def __init__(self):
        self.data = []

    def append(self, value):
        self.data.append(value)

    def pop(self):
        return self.data.pop(0)


class Input:

    def __init__(self):
        self.data = []

    def push(self, value):
        self.data.append(value)

    def pop(self, computer: 'Computer'):
        if not self.data:
            raise EOFError('No more input')
        return self.data.pop(0)


def move(computer: 'Computer', direction: int):
    assert direction in DIRS
    computer = deepcopy(computer)

    computer.input.push(direction)
    while not computer.output.data:
        computer.step()

    return computer.output.pop(), computer


class Computer:

    def __init__(self, mem: list[int], input: Input, output: Output):
        self.mem = defaultdict(
            lambda: 0, {
                i: val
                for i, val in enumerate(mem)
            }
        )
        self.input = input
        self.output = output

        self.pc = 0
        self.relative_base = 0
        self.running = True

    def __hash__(self):
        return hash(
            (
                tuple(self.mem.items()), self.pc, self.relative_base,
                self.running
            )
        )

    def run(self):
        while self.running:
            self.step()

    def step(self):
        assert self.running

        opcode = self.mem[self.pc]

        # parameter modes (0 = position, 1 = immediate, 2 = relative)
        mode1 = mode2 = mode3 = 0  # 'mode3' is unused
        if opcode >= 100:
            mode1 = (opcode % 10**3) // 10**2
            mode2 = (opcode % 10**4) // 10**3
            mode3 = opcode // 10**4
            opcode %= 100

        if opcode == 99:
            self.running = False

        # 1 parameter
        param1 = self.mem[self.pc + 1]
        if mode1 == REL:
            param1 += self.relative_base
        val1 = param1 if mode1 == IMM else self.mem[param1]

        if opcode == 3:
            self.mem[param1] = self.input.pop(self)
            self.pc += 2
            return

        if opcode == 4:
            self.output.append(val1)
            self.pc += 2
            return

        if opcode == 9:
            self.relative_base += val1
            self.pc += 2
            return

        # 2 parameters
        param2 = self.mem[self.pc + 2]
        if mode2 == REL:
            param2 += self.relative_base
        val2 = param2 if mode2 == IMM else self.mem[param2]

        if opcode == 5:  # if v1 != 0, self.pc = v2 (jump if true)
            self.pc = val2 if val1 != 0 else self.pc + 3
            return

        elif opcode == 6:  # if v1 == 0, self.pc = v2 (jump if false)
            self.pc = val2 if val1 == 0 else self.pc + 3
            return

        # 3 parameters
        param3 = self.mem[self.pc + 3]
        if mode3 == REL:
            param3 += self.relative_base
        # val3 = param3 if mode3 == IMM else self.mem[param3]

        if opcode == 7:  # if v1 < v2, vals[ind3] = 1, else 0 (less than)
            self.mem[param3] = int(val1 < val2)
            self.pc += 4
        elif opcode == 8:  # if v1 == v2, vals[ind3] = 1, else 0 (equals)
            self.mem[param3] = int(val1 == val2)
            self.pc += 4
        elif opcode == 1:
            self.mem[param3] = val1 + val2
            self.pc += 4
        elif opcode == 2:
            self.mem[param3] = val1 * val2
            self.pc += 4
        else:
            raise Exception(f'unknown opcode: {opcode}')


def part1(mem):
    input = Input()
    output = Output()
    computer = Computer(mem, input, output)

    q = [(0, 0, 0, computer)]
    seen = {(0, 0)}

    while q:
        steps, r, c, computer = q.pop(0)
        for d, (roff, coff) in zip(DIRS, DIR_OFFSETS):
            resp, newcomputer = move(computer, d)
            if resp == 1:
                newpos = (r + roff, c + coff)
                if newpos not in seen:
                    seen.add(newpos)
                    q.append((steps + 1, *newpos, newcomputer))
            if resp == 2:
                return steps + 1


def main():
    mem = list(map(int, sys.stdin.read().split(',')))

    a1 = part1(mem)
    print('part1:', a1)

    assert a1 == 234


if __name__ == '__main__':
    main()
