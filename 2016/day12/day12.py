import sys


class CPU:

    def __init__(self, mem: list[str]):
        self.pc = 0
        self.registers = dict(zip('abcd', [0] * 4))
        self.mem = mem

    def step(self):
        args = self.mem[self.pc].split()

        match args:
            case ['cpy', x, y]:
                self.registers[y] = self.parsevalue(x)
                self.pc += 1
            case ['inc', x]:
                self.registers[x] += 1
                self.pc += 1
            case ['dec', x]:
                self.registers[x] -= 1
                self.pc += 1
            case ['jnz', x, y]:
                if self.parsevalue(x):
                    self.pc += self.parsevalue(y)
                else:
                    self.pc += 1
            case _:
                raise Exception('unknown value')

        return self.pc < len(self.mem)

    def run(self):
        while self.step():
            pass

    def parsevalue(self, v: str):
        try:
            return int(v)
        except ValueError:
            return self.registers[v]


def main():
    lines = sys.stdin.read().strip().splitlines()

    cpu = CPU(lines)
    cpu.run()
    print('part1:', a1 := cpu.registers['a'])

    cpu = CPU(lines)
    cpu.registers['c'] = 1
    cpu.run()
    a2 = cpu.registers['a']
    print('part2:', a2 := cpu.registers['a'])

    assert a1 == 318117
    assert a2 == 9227771


if __name__ == '__main__':
    main()
