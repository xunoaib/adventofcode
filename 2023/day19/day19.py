#!/usr/bin/env python3
import json
import re
import sys
import operator


def make_rule(rulestr):
    args = re.split(r'[<>:]', rulestr)
    if len(args) == 1:
        return LiteralRule(rulestr)
    else:
        args.insert(1, '<' if '<' in rulestr else '>')
        return ConditionalRule(*args)


class LiteralRule:

    def __init__(self, value):
        self.value = value

    def __call__(self, part):
        return self.value


class ConditionalRule:

    def __init__(self, checkvar, opchar, checkval, retval):
        self.checkvar = checkvar
        self.opchar = opchar
        self.checkval = int(checkval)
        self.retval = retval
        self.opfunc = operator.lt if opchar == '<' else operator.gt

    def __call__(self, part):
        if self.opfunc(part[self.checkvar], self.checkval):
            return self.retval


class Workflow:

    def __init__(self, line):
        self.name, inner = re.search(r'(.*)\{(.*)\}', line).groups()
        self.rules = [make_rule(rulestr) for rulestr in inner.split(',')]

    def __call__(self, part):
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
        while (res := w(part)) not in 'RA':
            w = workflows[res]
        if res == 'A':
            a1 += sum(part.values())

    print('part1:', a1)


if __name__ == '__main__':
    main()
