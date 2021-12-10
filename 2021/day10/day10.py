#!/usr/bin/env python3
import sys

points = {')': 3, ']': 57, '}': 1197, '>': 25137}  # part1 scores for illegal chars
inc_scores = {')': 1, ']': 2, '}': 3, '>': 4}      # part2 scores for unused chars

pairs = {}
for k, v in zip('([{<', '>}])'[::-1]):
    pairs[v] = k
    pairs[k] = v

def find_corruption(line):
    """Find the first invalid character on a line, returning a tuple of its
    score and the list of incomplete/unused opening characters up until that point"""
    stack = []
    for ch in line:
        if ch in '{([<':
            stack.append(ch)
        else:
            opener = pairs[ch]
            if stack and stack[-1] == opener:
                stack.pop()
            else:
                return points[ch], stack
    return 0, stack

def part1(lines):
    return sum(list(zip(*map(find_corruption, lines)))[0])

def incomplete_score(stack):
    score = 0
    for ch in stack:
        score = (score * 5) + inc_scores[pairs[ch]]
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
