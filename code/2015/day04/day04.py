#!/usr/bin/env python3
import sys
from itertools import count
from hashlib import md5

def find_hash(key, find):
    for i in count(0):
        h = md5(f'{key}{i}'.encode()).hexdigest()
        if h.startswith(find):
            return i

def main():
    key = sys.stdin.read().strip()

    ans1 = find_hash(key, '0'*5)
    print('part1:', ans1)

    ans2 = find_hash(key, '0'*6)
    print('part2:', ans2)

    assert ans1 == 117946
    assert ans2 == 3938038

if __name__ == '__main__':
    main()
