import re

line = input()
result = ''

while m := re.search(r'\((\d+)x(\d+)\)', line):
    nchar, nrepeat = map(int, m.groups())
    result += line[:m.start()] + line[m.end():m.end() + nchar] * nrepeat
    line = line[m.end() + nchar:]

result += line

a1 = len(result)

print('part1:', a1)
