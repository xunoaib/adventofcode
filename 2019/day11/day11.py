#!/usr/bin/env python3
import sys
from collections import defaultdict

from PIL import Image


class Robot:
    def __init__(self, program):
        self.computer = Intcode(program)
        self.hull = defaultdict(int)
        self.pos = (0, 0)
        self.dir = 0
        self.painted = set()

    def run(self):
        while self.computer.running:
            r, c = self.pos
            input_val = self.hull[(r, c)]

            color = self.computer.run(input_val)
            if color is None:
                break
            turn = self.computer.run(None)

            self.hull[(r, c)] = color
            self.dir += turn or -1
            self.dir %= 4
            # print(f'painting {self.pos} {color}, turning {turn} (now {self.dir})')
            self.painted.add(self.pos)

            # move forward
            roff, coff = {
                0: (-1, 0),
                1: (0, 1),
                2: (1, 0),
                3: (0, -1),
            }[self.dir]

            self.pos = (r + roff, c + coff)
        return len(self.painted)


class Intcode:
    POS, IMM, REL = 0, 1, 2

    def __init__(self, program):
        self.pc = 0
        self.relative_base = 0
        self.running = True
        self.mem = defaultdict(lambda: 0,
                               {i: val
                                for i, val in enumerate(program)})

    def run(self, input_val):
        while True:
            opcode = self.mem[self.pc]

            # parameter modes (0 = position, 1 = immediate, 2 = relative)
            mode1 = mode2 = mode3 = 0  # 'mode3' is unused
            if opcode >= 100:
                mode1 = (opcode % 10**3) // 10**2
                mode2 = (opcode % 10**4) // 10**3
                mode3 = (opcode % 10**5) // 10**4
                opcode %= 100


            if opcode == 99:
                self.running = False
                return None

            # 1 parameter
            param1 = self.mem[self.pc + 1]
            if mode1 == self.REL:
                param1 += self.relative_base
            val1 = param1 if mode1 == self.IMM else self.mem[param1]

            if opcode == 3:
                if input_val is None:
                    print('invalid read!')
                    exit()
                self.mem[param1] = input_val  # robot.read_tile()
                self.pc += 2
                continue

            if opcode == 4:
                self.pc += 2
                return val1

            if opcode == 9:
                self.relative_base += val1
                self.pc += 2
                continue

            # 2 parameters
            param2 = self.mem[self.pc + 2]
            if mode2 == self.REL:
                param2 += self.relative_base
            val2 = param2 if mode2 == self.IMM else self.mem[param2]

            if opcode == 5:  # if v1 != 0, self.pc = v2 (jump if true)
                self.pc = val2 if val1 != 0 else self.pc + 3
                continue

            elif opcode == 6:  # if v1 == 0, pc = v2 (jump if false)
                self.pc = val2 if val1 == 0 else self.pc + 3
                continue

            # 3 parameters
            param3 = self.mem[self.pc + 3]
            if mode3 == self.REL:
                param3 += self.relative_base
            # val3 = param3 if mode3 == self.IMM else self.mem[param3]

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
                print('unknown opcode:', opcode)
                exit()


def visualize(hull):
    points = [pt for pt, val in hull.items() if val == 1]

    ys, xs = zip(*points)
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    width = xmax - xmin + 1
    height = ymax - ymin + 1

    image = Image.new('1', (width, height))
    for y, x in points:
        image.putpixel((x - xmin, y - ymin), 1)

    image = image.resize((width * 10, height * 10), Image.ANTIALIAS)
    image.show()


def main():
    lines = sys.stdin.read().strip().split(',')
    program = list(map(int, lines))

    robot = Robot(program)
    ans1 = robot.run()
    print('part1:', ans1)

    robot = Robot(program)
    robot.hull[robot.pos] = 1
    ans2 = robot.run()
    visualize(robot.hull)

if __name__ == '__main__':
    main()
