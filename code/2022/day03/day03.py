#!/usr/bin/env python3
import sys
import string

def main():
    lines = sys.stdin.read().splitlines()

    priorities = {ch: ord(ch) - ord('a') + 1 for ch in string.ascii_lowercase}
    priorities.update({ch: ord(ch) - ord('A') + 27 for ch in string.ascii_uppercase})

    part1 = 0
    for line in lines:
        a = line[:len(line)//2]
        b = line[len(line)//2:]
        overlap = set(a) & set(b)
        part1 += sum(priorities[ch] for ch in overlap)
    print('part1:', part1)

    part2 = 0
    for i in range(0, len(lines), 3):
        x,y,z = [set(sack) for sack in lines[i:i+3]]
        overlap = x & y & z
        part2 += sum(priorities[ch] for ch in overlap)
    print('part2:', part2)

    assert part1 == 7742
    assert part2 == 2276

if __name__ == '__main__':
    main()
