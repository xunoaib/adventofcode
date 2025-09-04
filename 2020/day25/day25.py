#!/usr/bin/env python
import sys

def find_loop(subject, target):
    value = 1
    iteration = 0
    while value != target:
        value *= subject
        value %= 20201227
        iteration += 1
    return iteration

pub1, pub2 = map(int, sys.stdin)

# loop1 = find_loop(7, pub1)
# print(pow(pub2, loop1, 20201227))

loop2 = find_loop(7, pub2)
print(pow(pub1, loop2, 20201227))
