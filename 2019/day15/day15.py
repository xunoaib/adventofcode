#!/usr/bin/env python3
import sys
from collections import defaultdict
from itertools import batched

POS, IMM, REL = 0, 1, 2


class Output:

    def __init__(self):
        self.data = []

    def append(self, value):
        self.data.append(value)


class Input:

    def next(self, output: Output):
        # TODO: solution moves
        return -1


def run_simulation(
    mem,
    input: Input,
    output: Output,
):
    mem = defaultdict(lambda: 0, {i: val for i, val in enumerate(mem)})
    pc = relative_base = 0
    last_output = None

    while True:
        opcode = mem[pc]

        # parameter modes (0 = position, 1 = immediate, 2 = relative)
        mode1 = mode2 = mode3 = 0  # 'mode3' is unused
        if opcode >= 100:
            mode1 = (opcode % 10**3) // 10**2
            mode2 = (opcode % 10**4) // 10**3
            mode3 = opcode // 10**4
            opcode %= 100

        if opcode == 99:
            break

        # 1 parameter
        param1 = mem[pc + 1]
        if mode1 == REL:
            param1 += relative_base
        val1 = param1 if mode1 == IMM else mem[param1]

        if opcode == 3:
            mem[param1] = input.next(output)
            pc += 2
            continue

        if opcode == 4:
            output.append(val1)
            last_output = val1
            pc += 2
            continue

        if opcode == 9:
            relative_base += val1
            pc += 2
            continue

        # 2 parameters
        param2 = mem[pc + 2]
        if mode2 == REL:
            param2 += relative_base
        val2 = param2 if mode2 == IMM else mem[param2]

        if opcode == 5:  # if v1 != 0, pc = v2 (jump if true)
            pc = val2 if val1 != 0 else pc + 3
            continue

        elif opcode == 6:  # if v1 == 0, pc = v2 (jump if false)
            pc = val2 if val1 == 0 else pc + 3
            continue

        # 3 parameters
        param3 = mem[pc + 3]
        if mode3 == REL:
            param3 += relative_base
        # val3 = param3 if mode3 == IMM else mem[param3]

        if opcode == 7:  # if v1 < v2, vals[ind3] = 1, else 0 (less than)
            mem[param3] = int(val1 < val2)
            pc += 4
        elif opcode == 8:  # if v1 == v2, vals[ind3] = 1, else 0 (equals)
            mem[param3] = int(val1 == val2)
            pc += 4
        elif opcode == 1:
            mem[param3] = val1 + val2
            pc += 4
        elif opcode == 2:
            mem[param3] = val1 * val2
            pc += 4
        else:
            print('unknown opcode:', opcode)
            return


def part1(mem):
    input = Input()
    output = Output()
    run_simulation(mem, input, output)


def main():
    mem = list(map(int, sys.stdin.read().split(',')))

    a1 = part1(mem)
    print('part1:', a1)


if __name__ == '__main__':
    main()
