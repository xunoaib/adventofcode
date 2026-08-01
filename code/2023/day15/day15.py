#!/usr/bin/env python3
import sys


def hashit(line, v):
    v = 0
    for c in line:
        v += ord(c)
        v *= 17
        v %= 256
    return v


def part2(lines):
    boxes = [[] for _ in range(256)]
    for line in lines:
        label, *flen = line.split('=')
        label = label.split('-')[0]
        boxid = hashit(label, 0)

        if line[-1] == '-':
            boxes[boxid] = [lens for lens in boxes[boxid] if lens[0] != label]
        else:
            new = (label, int(flen[0]))
            for idx, lens in enumerate(boxes[boxid]):
                if lens[0] == label:
                    boxes[boxid][idx] = new
                    break
            else:
                boxes[boxid].append(new)

    ans = 0
    for boxnum, box in enumerate(boxes):
        for lnum, (label, flen) in enumerate(box):
            ans += (1 + boxnum) * (1 + lnum) * flen
    return ans


def main():
    lines = sys.stdin.read().strip().split(',')

    v = 0
    a1 = sum(v := hashit(line, v) for line in lines)
    a2 = part2(lines)

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 512283
    assert a2 == 215827


if __name__ == '__main__':
    main()
