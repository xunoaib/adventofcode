#!/usr/bin/env python3
import re
import sys
import numpy as np

def run1(arr, line):
    action, pt1, pt2 = re.match(r'(.*) (\S+) through (.*)', line).groups()
    x1,y1 = map(int, pt1.split(','))
    x2,y2 = map(int, pt2.split(','))

    if action == 'turn on':
        arr[x1:x2+1,y1:y2+1] = 1
    elif action == 'turn off':
        arr[x1:x2+1,y1:y2+1] = 0
    elif action == 'toggle':
        arr[x1:x2+1,y1:y2+1] = ~arr[x1:x2+1,y1:y2+1]

def run2(arr, line):
    action, pt1, pt2 = re.match(r'(.*) (\S+) through (.*)', line).groups()
    x1,y1 = map(int, pt1.split(','))
    x2,y2 = map(int, pt2.split(','))

    region = arr[x1:x2+1,y1:y2+1]
    if action == 'turn on':
        region += 1
    elif action == 'turn off':
        region -= 1
        region[region < 0] = 0
    elif action == 'toggle':
        region += 2

def part1(lines):
    arr = np.zeros((1000, 1000), dtype=bool)
    for line in lines:
        run1(arr, line)
    return len(arr[arr == True])

def part2(lines):
    arr = np.zeros((1000, 1000))
    for line in lines:
        run2(arr, line)
    return int(arr.sum())

def main():
    lines = sys.stdin.read().strip().split('\n')

    ans1 = part1(lines)
    print('part1:', ans1)

    ans2 = part2(lines)
    print('part2:', ans2)

    assert ans1 == 569999
    assert ans2 == 17836115

if __name__ == '__main__':
    main()
