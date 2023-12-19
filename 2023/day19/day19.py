#!/usr/bin/env python3
import copy
import json
import operator
import re
import sys

# This is extremely messy. I apologize...

class TreeNode:

    def __init__(self, value=None, left=None, right=None):
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return f'T({self.value})'

    def isleaf(self):
        return self.value in list('RA')


def make_rule(rulestr):
    args = re.split(r'[<>:]', rulestr)
    if len(args) == 1:
        return args[0]
    args.insert(1, '<' if '<' in rulestr else '>')
    return ConditionalRule(*args)


class ConditionalRule:

    def __init__(self, checkvar, opchar, checkval, retval):
        self.checkvar = checkvar
        self.opchar = opchar
        self.checkval = int(checkval)
        self.opfunc = operator.lt if opchar == '<' else operator.gt
        self.retval = retval

    def __call__(self, part):
        if self.opfunc(part[self.checkvar], self.checkval):
            return self.retval

    def __repr__(self):
        return f'CR({self.checkvar}{self.opchar}{self.checkval}:{self.retval})'


class Workflow:

    def __init__(self, line):
        self.name, self.inner = re.search(r'(.*)\{(.*)\}', line).groups()
        self.rules = [make_rule(rulestr) for rulestr in self.inner.split(',')]

    def __call__(self, part):
        for rule in self.rules[:-1]:
            if (res := rule(part)) is not None:
                return res
        return self.rules[-1]

    def __repr__(self):
        return f'Workflow({self.name}, {self.inner})'


class Ranges:

    def __init__(self):
        self.mins = dict(zip('xmas', [1] * 4))
        self.maxs = dict(zip('xmas', [4000] * 4))

    def update_min(self, var, val):
        self.mins[var] = max(self.mins[var], val)

    def update_max(self, var, val):
        self.maxs[var] = min(self.maxs[var], val)

    def __len__(self):
        p = 1
        for v in self.mins:
            t = max(0, self.maxs[v] - self.mins[v] + 1)
            p *= t
        return p

    def __repr__(self):
        vs = [f'{v}=[{self.mins[v]},{self.maxs[v]}]' for v in self.mins]
        vs = [f'{v:<13}' for v in vs]
        return 'Ranges({})'.format('  '.join(vs))

    def split(self, rule: ConditionalRule):
        '''Splits the current range into two new ranges based on a condition'''

        var = rule.checkvar
        val = rule.checkval
        true, false = copy.deepcopy(self), copy.deepcopy(self)
        if rule.opchar == '<':
            true.update_max(var, val - 1)
            false.update_min(var, val)
        else:  # var > val
            true.update_min(var, val + 1)
            false.update_max(var, val)
        return true, false


def print_tree(tree, d=0):
    if not tree:
        return
    print(' ' * d + '-', tree.value)
    if tree.right:
        print_tree(tree.right, d + 2)
    if tree.left:
        print_tree(tree.left, d + 2)


class Part2:

    def __init__(self, workflows):
        self.workflows = workflows
        self.leafranges = []
        self.paths = []

    def build_workflow_tree(self, workflow: Workflow):
        nodes = [TreeNode(value=rule) for rule in workflow.rules]
        for i, node in enumerate(nodes[:-1]):
            node.left = nodes[i + 1]
            trueval = workflow.rules[i].retval
            if trueval in 'RA':
                node.right = TreeNode(value=trueval)
            else:
                node.right = self.build_workflow_tree(self.workflows[trueval])
        return nodes[0]

    def count(self, node: TreeNode, ranges: Ranges, path=tuple()):
        path += (node, )
        if node.isleaf():  # A or R
            if node.value == 'A':  # and len(ranges):
                self.leafranges.append(ranges)
                self.paths.append(path)
                return len(ranges)
            return 0
        elif isinstance(node.value, ConditionalRule):
            t, f = ranges.split(node.value)
            tcount = self.count(node.left, f, path)
            fcount = self.count(node.right, t, path)
            return tcount + fcount
        else:  # workflow id
            workflow = self.workflows[node.value]
            newnode = self.build_workflow_tree(workflow)
            return self.count(newnode, ranges, path)
        return 0

    def solve(self):
        tree = self.build_workflow_tree(self.workflows['in'])
        return self.count(tree, Ranges())


def main():
    _ws, parts = [
        line.split('\n') for line in sys.stdin.read().strip().split('\n\n')
    ]

    workflows = {}
    for line in _ws:
        wf = Workflow(line)
        workflows[wf.name] = wf

    a1 = 0
    for line in parts:
        part = json.loads(re.sub(r'([xmas])', r'"\1"', line.replace('=', ':')))
        w = workflows['in']
        while (res := w(part)) not in 'RA':
            w = workflows[res]
        if res == 'A':
            a1 += sum(part.values())

    a2 = Part2(workflows).solve()

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 377025
    assert a2 == 135506683246673


if __name__ == '__main__':
    main()
