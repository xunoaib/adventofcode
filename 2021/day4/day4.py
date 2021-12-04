#!/usr/bin/env python3
import copy
import re
import sys
import numpy as np

def mark_board(board, num):
    ''' Update a bingo board with the called number '''
    for r, row in enumerate(board):
        board[r] = [None if n == num else n for n in row]

def has_won(board):
    ''' Look for 5 marked cells in any row or column '''
    if [None]*5 in board:
        return True
    rot = np.rot90(np.array(board), 1, (0,1))
    return any(list(row) == [None]*5 for row in rot)

def calc_score(board, num):
    ''' Return the sum of all unmarked cells multiplied by the winning bingo number '''
    return sum([v for row in board for v in row if v is not None]) * num

def part1(numbers, boards):
    ''' Play rounds until one board wins. Returns the score of the winning board '''
    boards = copy.deepcopy(boards)
    for num in numbers:
        for i, board in enumerate(boards):
            mark_board(board, num)
            if has_won(board):
                return calc_score(board, num)
    return None, None

def part2(numbers, boards):
    ''' Play rounds until all boards have won. Returns the score of the last winning board '''
    boards = copy.deepcopy(boards)
    for num in numbers:
        for i, board in list(enumerate(boards)):
            mark_board(board, num)
            if has_won(board):
                boards.remove(board)
                if len(boards) == 0:
                    return calc_score(board, num)
    return None, None

def main():
    numbers = list(map(int, sys.stdin.readline().split(',')))
    boards = []
    for line in sys.stdin:
        if line == '\n':
            boards.append([])
            continue
        row = list(map(int, re.split(r'\s+', line.strip())))
        boards[-1].append(row)

    ans1 = part1(numbers, boards)
    ans2 = part2(numbers, boards)
    print('part1:', ans1)
    print('part2:', ans2)
    assert ans1 == 41503
    assert ans2 == 3178

if __name__ == '__main__':
    main()
