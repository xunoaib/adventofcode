#!/usr/bin/env python3
import re
import sys

def has_abba(data):
    for i in range(len(data) - 3):
        s = data[i:i+4]
        if s[0] == s[3] and s[1] == s[2] and s[0] != s[1]:
            return True
    return False

# note: aba/bab have identical validation rules
def is_aba(aba):
    return aba[0] == aba[2] and aba[0] != aba[1]

def is_ssl(supernets, hypernets):
    # keep track of all ABA sequences
    abas = set()

    # gather valid ABAs
    for supernet in supernets:
        for i in range(len(supernet) - 2):
            aba = supernet[i:i+3]
            if is_aba(aba):
                abas.add(aba)

    # gather BABs, convert to ABA, then check if they exist in the ABAs set
    for hypernet in hypernets:
        for i in range(len(hypernet) - 2):
            bab = hypernet[i:i+3]
            aba = bab[1] + bab[0] + bab[1]
            if is_aba(bab) and aba in abas:
                return True
    return False

def main():
    lines = sys.stdin.read().strip().splitlines()

    all_supernets = [re.sub(r'\[(.*?)\]', ' ', line).split(' ') for line in lines]
    all_hypernets = [re.findall(r'\[(.*?)\]', line) for line in lines]

    part1 = 0
    for supernets, hypernets in zip(all_supernets, all_hypernets):
        if not any(map(has_abba, hypernets)) \
                and any(map(has_abba, supernets)):
            part1 += 1
    print('part1:', part1)

    part2 = 0
    for supernets, hypernets, line in zip(all_supernets, all_hypernets, lines):
        if is_ssl(supernets, hypernets):
            part2 += 1
    print('part2:', part2)

    assert part1 == 110
    assert part2 == 242

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
