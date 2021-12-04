#!/usr/bin/env python3
import copy
import re
import sys

def has_won(board):
    ''' Look for 5 marked cells in any row or column '''
    return [None]*5 in board or (None,)*5 in list(zip(*board))

def mark_board(board, num):
    ''' Update a bingo board with the given number. Returns whether it was a winning move '''
    for r, row in enumerate(board):
        board[r] = [None if n == num else n for n in row]
    return has_won(board)

def calc_score(board, num):
    ''' Return the sum of all unmarked cells multiplied by the winning bingo number '''
    return sum([v for row in board for v in row if v is not None]) * num

def part1(numbers, boards):
    ''' Play rounds until one board wins. Returns the score of the winning board '''
    boards = copy.deepcopy(boards)
    for num in numbers:
        for i, board in enumerate(boards):
            if mark_board(board, num):
                return calc_score(board, num)

def part2(numbers, boards):
    ''' Play rounds until all boards have won. Returns the score of the last winning board '''
    boards = copy.deepcopy(boards)
    for num in numbers:
        for i, board in list(enumerate(boards)):
            if mark_board(board, num):
                boards.remove(board)
                if len(boards) == 0:
                    return calc_score(board, num)

def main():
    numbers = list(map(int, sys.stdin.readline().split(',')))
    groups = sys.stdin.read().strip().split('\n\n')
    boards = [[list(map(int, re.split(r'\s+', line.strip()))) for line in group.split('\n')] for group in groups]

    ans1 = part1(numbers, boards)
    ans2 = part2(numbers, boards)

    print('part1:', ans1)
    print('part2:', ans2)
    assert ans1 == 41503
    assert ans2 == 3178

if __name__ == '__main__':
    main()
