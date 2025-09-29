import re


def part1(line: str):
    result = ''

    while m := re.search(r'\((\d+)x(\d+)\)', line):
        nchar, nrepeat = map(int, m.groups())
        result += line[:m.start()] + line[m.end():m.end() + nchar] * nrepeat
        line = line[m.end() + nchar:]

    return len(result + line)


line = input()

a1 = part1(line)

print('part1:', a1)
