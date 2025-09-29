import sys


class CPU:

    def __init__(self, commands: list[str]):
        self.commands = commands
        self.regs = {'a': 0, 'b': 0}
        self.pc = 0

    def step(self):
        if self.pc >= len(self.commands) or self.pc < 0:
            return False

        args = self.commands[self.pc].split()

        match args:
            case 'hlf', r:
                self.regs[r] //= 2
                self.pc += 1
            case 'tpl', r:
                self.regs[r] *= 3
                self.pc += 1
            case 'inc', r:
                self.regs[r] += 1
                self.pc += 1
            case 'jmp', offset:
                self.pc += int(offset)
            case 'jie', r, offset:
                if self.regs[r] % 2 == 0:
                    self.pc += int(offset)
                else:
                    self.pc += 1
            case 'jio', r, offset:
                if self.regs[r] == 1:
                    self.pc += int(offset)
                else:
                    self.pc += 1
            case _:
                raise ValueError('unknown')

        return True

    def run(self):
        while self.step():
            pass


cmds = sys.stdin.read().replace(',', '').splitlines()

cpu = CPU(cmds)
cpu.run()
a1 = cpu.regs['b']

cpu = CPU(cmds)
cpu.regs['a'] = 1
cpu.run()
a2 = cpu.regs['b']

print('part1:', a1)
print('part2:', a2)

assert a1 == 184
assert a2 == 231
