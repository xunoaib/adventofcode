import re

line = input()
result = ''

while True:
    if m := re.search(r'\((\d+)x(\d+)\)', line):
        nchar, nrepeat = map(int, m.groups())
        result += line[:m.start()] + line[m.end():m.end() + nchar] * nrepeat
        line = line[m.end() + nchar:]
    else:
        result += line
        break

a1 = len(result)

print('part1:', a1)
