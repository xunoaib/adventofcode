#!/usr/bin/env python3
import json
import sys
from collections import defaultdict, Counter
from itertools import permutations

lookup = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg',
}
invlookup = {v:k for k,v in lookup.items()}

# maps length to possible numbers
lengths = defaultdict(set)
for num, segments in lookup.items():
    lengths[len(segments)].add(num)
lengths = dict(lengths)

# map unique segment length to KNOWN digit
known = {slen:list(nums)[0] for slen,nums in lengths.items() if len(nums) == 1}

# map wires to the digits that use them
used_wires = defaultdict(set)
for num, segments in lookup.items():
    for wire in segments:
        used_wires[wire].add(num)
used_wires = dict(used_wires)

# -----------------------
def newsolve():
    # patterns = sorted(''.join(sorted(g)) for g in sys.stdin.readline().split(' | ')[0].split())
    # print('\n'.join(patterns))

    # from known data, associate segment counts (across all digits) to their possible segments
    # print(' '.join(lookup.values()).upper())
    segment_counts = Counter(''.join(lookup.values()).upper())
    counts_to_segments = defaultdict(set)
    for segment, count in segment_counts.items():
        counts_to_segments[count].add(segment)
    counts_to_segments = dict(counts_to_segments)
    # print(segment_counts)
    print('counts -> segments:', counts_to_segments)

    # from unknown data, deduce real segment candidates based on scrambled segment counts
    scrambled_counts = Counter(''.join(patterns))
    candidates = {segment: counts_to_segments[count] for segment, count in scrambled_counts.items()}
    # print(candidates)

    # assign any conclusive candidates
    for segment, candset in candidates.items():
        if len(candset) == 1:
            print(segment, '->', list(candset)[0])
        else:
            print(segment, '->', sorted(candset))

    # permute remaining candidates

def part1_count(line):
    g1, g2 = ((list(map(lambda s: ''.join(sorted(s)), side.split(' ')))) for side in line.split(' | '))
    count = 0
    for pattern in g2:
        if len(pattern) in known:
            count += 1
    return count

def validate(patterns):
    return len(set(patterns) - set(lookup.values())) == 0

def decode(line):
    # generate all possible wire substitutions/descrambling configurations
    for perm in permutations('abcdefg'):
        # descramble with string substitution
        temp = line.upper()
        for srch, repl in zip('ABCDEFG', perm):
            temp = temp.replace(srch, repl)

        # decode and return value if descrambled wire configuration is valid
        g1, g2 = ((list(map(lambda s: ''.join(sorted(s)), side.split(' ')))) for side in temp.split(' | '))
        if validate(g1 + g2):
            return int(''.join(str(invlookup[pattern]) for pattern in g2), 10)

def part1(lines):
    return sum(map(part1_count, lines))

def part2(lines):
    return sum(map(decode, lines))

def main():
    lines = sys.stdin.read().strip().split('\n')

    ans1 = part1(lines)
    print('part1:', ans1)

    ans2 = part2(lines)
    print('part2:', ans2)

    assert ans1 == 525
    assert ans2 == 1083859

if __name__ == '__main__':
    main()
