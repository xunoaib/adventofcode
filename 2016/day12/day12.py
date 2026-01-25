import sys


class CPU:

    def __init__(self):
        self.registers = [0] * 4

    def execute(self, inst: str):
        args = inst.split()
        print(repr(inst))
        match args:
            case ['cpy', x, y]:
                self.registers[ord(y) - ord('a')] = int(x) if x.isdigit(
                ) else self.registers[ord(x) - ord('a')]
            case _:
                print('unknown instruction')


def main():
    cpu = CPU()

    lines = sys.stdin.read().strip().splitlines()

    for line in lines:
        cpu.execute(line)


if __name__ == '__main__':
    main()
