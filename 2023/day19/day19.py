#!/usr/bin/env python3
import json
import re
import sys
import operator


def make_rule(rulestr):
    args = re.split(r'[<>:]', rulestr)
    if len(args) == 1:
        return lambda p: args[0]
    else:
        op = operator.lt if '<' in rulestr else operator.gt
        return lambda p: args[2] if op(p[args[0]], int(args[1])) else None


class Workflow:

    def __init__(self, line):
        self.name, inner = re.search(r'(.*)\{(.*)\}', line).groups()
        self.rules = [make_rule(rulestr) for rulestr in inner.split(',')]

    def process(self, part):
        for rule in self.rules:
            if (res := rule(part)) is not None:
                return res


def main():
    _ws, _rs = [
        line.split('\n') for line in sys.stdin.read().strip().split('\n\n')
    ]

    workflows = {}
    for line in _ws:
        wf = Workflow(line)
        workflows[wf.name] = wf

    a1 = 0
    for line in _rs:
        part = json.loads(re.sub(r'([xmas])', r'"\1"', line.replace('=', ':')))
        w = workflows['in']
        while (res := w.process(part)) not in 'RA':
            w = workflows[res]
        if res == 'A':
            a1 += sum(part.values())

    print('part1:', a1)

if __name__ == '__main__':
    main()
