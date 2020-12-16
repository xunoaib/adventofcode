#!/usr/bin/env python
import sys
import parse

def check_password_part1(line):
    a, b, char, password = parse.parse('{:d}-{:d} {}: {}', line)
    return a <= password.count(char) <= b

def check_password_part2(line):
    a, b, char, password = parse.parse('{:d}-{:d} {}: {}', line)
    ch1 = password[a-1]
    ch2 = password[b-1]
    return (ch1, ch2).count(char) == 1

count1 = 0
count2 = 0

for line in sys.stdin:
    if check_password_part1(line):
        count1 += 1
    if check_password_part2(line):
        count2 += 1

print('part1 matches:', count1)
print('part2 matches:', count2)
