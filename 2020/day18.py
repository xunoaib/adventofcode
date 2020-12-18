#!/usr/bin/env python
import sys
import operator

operators = {
    '+': operator.add,
    '*': operator.mul,
    '-': operator.sub,
}

def evaluate_part1(line):
    stack = []
    for ch in line:
        if '0' <= ch <= '9':
            acc = int(ch)
            if len(stack) and stack[-1] != '(':
                op, val = stack.pop(), stack.pop()
                acc = op(val, acc)
            stack.append(acc)
        elif ch == ')':
            acc = stack.pop()
            assert stack.pop() == '('
            if len(stack) and stack[-1] != '(':
                op, val = stack.pop(), stack.pop()
                acc = op(val, acc)
            stack.append(acc)
        elif op := operators.get(ch):
            stack.append(op)
        else:
            stack.append(ch)
    return stack[0]

def evaluate_part2(line):
    stack = []
    for ch in line:
        if '0' <= ch <= '9':
            stack.append(int(ch))
        elif ch == ')':
            acc = stack.pop()
            while stack[-1] != '(':
                op, val = stack.pop(), stack.pop()
                acc = op(val, acc)
            stack.pop() # pop paren
            stack.append(acc)
        elif op := operators.get(ch):
            stack.append(op)
        else:
            stack.append(ch)

        # always perform addition if possible
        if len(stack) > 1 and stack[-1] != '(' and stack[-2] == operator.add:
            top, op, bot = stack.pop(), stack.pop(), stack.pop()
            acc = op(bot, top)
            stack.append(acc)

    # evaluate the remaining expression
    acc = stack.pop()
    while len(stack):
        op, bot = stack.pop(), stack.pop()
        acc = op(bot, acc)
    return acc

lines = [line.strip().replace(' ','') for line in sys.stdin]

total = sum(map(evaluate_part1, lines))
print('part1:', total)
assert total == 3885386961962

total = sum(map(evaluate_part2, lines))
print('part2:', total)
assert total == 112899558798666
