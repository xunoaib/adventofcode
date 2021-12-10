#!/usr/bin/env python3
import re
import sys

points = {')': 3, ']': 57, '}': 1197, '>': 25137}  # part1 scores for illegal chars
unmatched_scores = '([{<'  # str.index(ch) + 1 => unmatched character score

def simplify(line):
    """Iteratively remove adjacent opening/closing pairs"""
    replaced = True
    while replaced:
        replaced = False
        for ch in ['()', '{}', '[]', '<>']:
            if ch in line:
                replaced = True
                line = line.replace(ch, '')
    return line

def find_corruption(line):
    line = simplify(line)
    if m := re.search('([' + re.escape('>])}') + '])', line):
        return points[m.group(0)], line
    return 0, line

def part1(lines):
    return sum(list(zip(*map(find_corruption, lines)))[0])

def incomplete_score(stack):
    score = 0
    for ch in stack:
        score = score * 5 + unmatched_scores.index(ch) + 1
    return score

def part2(lines):
    scores = []
    for line in lines:
        score, stack = find_corruption(line)
        if score == 0:
            new_score = incomplete_score(stack[::-1])
            scores.append(new_score)
    return sorted(scores)[len(scores) // 2]

def main():
    lines = sys.stdin.read().strip().split()

    ans1 = part1(lines)
    print('part1:', ans1)

    ans2 = part2(lines)
    print('part2:', ans2)

    assert ans1 == 271245
    assert ans2 == 1685293086

if __name__ == '__main__':
    main()
