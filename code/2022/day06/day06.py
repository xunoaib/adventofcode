#!/usr/bin/env python3
import sys

def main():
    line = sys.stdin.read().strip()

    for i,_ in enumerate(line[:-4]):
        chars = line[i:i+4]
        if len(set(chars)) == 4:
            print('part1:', i + 4)
            break

    for i,_ in enumerate(line[:-14]):
        chars = line[i:i+14]
        if len(set(chars)) == 14:
            print('part2:', i + 14)
            break

if __name__ == '__main__':
    main()
