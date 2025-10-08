import bisect
import sys
from collections import defaultdict
from functools import cache

# TODO: Find line equations instead of brute forcing

POS, IMM, REL = 0, 1, 2
DIR_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Computer:

    def __init__(self, mem: list[int]):
        self.mem = defaultdict(
            lambda: 0, {
                i: val
                for i, val in enumerate(mem)
            }
        )
        self.input: list[int] = []
        self.output: list[int] = []

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
            self.mem[param1] = self.input.pop(0)
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
            self.running = False


def part1(mem):
    total = 0
    for r in range(50):
        for c in range(50):
            computer = Computer(mem)
            computer.input = [r, c]
            computer.run()
            total += computer.output[0]
    return total


class LazySeq:

    def __init__(self, n, f):
        self.n = n
        self.f = cache(f)

    def __len__(self):
        return self.n

    def __getitem__(self, i):
        if 0 <= i < self.n:
            return self.f(i)
        raise IndexError


def part2(mem):
    count = lambda r: count_diag(r, mem)
    seq = LazySeq(4096, count)

    r = 1 + bisect.bisect_left(seq, 99)
    while count(r) < 100:
        r += 1
        print('trying r =', r)

    start_row = r

    vals = [
        (r, start_row - r) for r in range(start_row + 1)
        if detect(r, start_row - r, mem)
    ]

    (rmin, cmin), (rmax, cmax) = min(vals), max(vals)

    r = min(cmin, cmax)
    c = min(rmin, rmax)
    return c * 10000 + r


def detect(row: int, col: int, mem: list[int]):
    computer = Computer(mem)
    computer.input = [row, col]
    computer.run()
    return computer.output[0]


def count_diag(start_row: int, mem: list[int]):
    total = 0
    for r in range(start_row + 1):
        total += detect(r, start_row - r, mem)
    return total


def main():
    mem = list(map(int, sys.stdin.read().split(',')))

    a1 = part1(mem)
    print('part1:', a1)

    a2 = part2(mem)
    print('part2:', a2)

    assert a1 == 112
    assert a2 == 18261982


if __name__ == '__main__':
    main()
