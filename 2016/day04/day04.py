#!/usr/bin/env python3
import re
import sys
from collections import Counter

def main():
    lines = sys.stdin.read().strip().split('\n')

    total = 0
    part2 = None

    for line in lines:
        chars, sid, checksum = re.match(r'(.*)-(\d+)\[(.*)\]', line).groups()
        sid = int(sid)
        counts = Counter(chars.replace('-', ''))
        pairs = sorted(counts.most_common(), key=lambda kv: (-kv[1], kv[0]))
        checksum_calc = ''.join(p[0] for p in pairs[:5])
        if checksum_calc == checksum:
            total += sid

        dec = ''.join(chr((ord(c) - ord('a') + sid) % 26 + ord('a')) if c != '-' else c for c in chars )
        if re.search(r'north.*pole', dec):
            part2 = sid

    print('part1:', total)
    print('part2:', part2)

if __name__ == "__main__":
    main()
