import re


def part1(line: str):
    result = ''

    while m := re.search(r'\((\d+)x(\d+)\)', line):
        nchar, nrepeat = map(int, m.groups())
        result += line[:m.start()] + line[m.end():m.end() + nchar] * nrepeat
        line = line[m.end() + nchar:]

    return len(result + line)


def part2(line: str) -> int:
    count = 0

    while m := re.search(r'\((\d+)x(\d+)\)', line):
        nchar, nrepeat = map(int, m.groups())
        s = line[m.end():m.end() + nchar]
        count += len(line[:m.start()]) + part2(s) * nrepeat
        line = line[m.end() + nchar:]

    return count + len(line)


def main():
    line = input()

    a1 = part1(line)
    a2 = part2(line)

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 99145
    assert a2 == 10943094568


if __name__ == '__main__':
    main()
