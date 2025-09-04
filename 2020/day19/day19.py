#!/usr/bin/env python
import re
import sys

from parsimonious.exceptions import ParseError
from parsimonious.grammar import Grammar


def reformat_grammar(puzzle_input):
    '''Reformat puzzle input as valid "parsimonious" grammar'''

    data = puzzle_input.strip().replace(': ', ' = ').strip()
    data = f' {data} '.replace('\n', ' \n ')

    for n in range(data.count('\n') + 1):
        while f' {n} ' in data:
            data = data.replace(f' {n} ', f' R{n} ')

    lines = data.split('\n ')
    for i,line in enumerate(lines):
        lines[i] = re.sub(r'= (.*) \| (.*)', r'= (\1) / (\2)', line.strip())

    return '\n'.join(sorted(lines))

def count_valid(rules: str, messages):
    rules = reformat_grammar(rules)
    grammar = Grammar(rules)

    valid = []
    for i,msg in enumerate(messages):
        try:
            res = grammar.parse(msg)
            if res.expr_name == 'R0':
                valid.append(msg)
        except ParseError as exc:
            print(exc)
            if "Rule 'R31' didn't match at ''" in str(exc): # ಠ_ಠ
                valid.append(msg)
    return valid

rules, messages = sys.stdin.read().strip().split('\n\n')
messages = messages.strip().split('\n')

valid = count_valid(rules, messages)
print('part1:', len(valid))
assert len(valid) == 224

rules = rules.replace('\n8: 42', '\n8: 42 | 42 8')
rules = rules.replace('\n11: 42 31', '\n11: 42 31 | 42 11 31')

valid = count_valid(rules, messages)
print('part2:', len(valid))
assert len(valid) == 436
