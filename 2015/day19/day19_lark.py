import pickle
import re
import sys
from collections import defaultdict
from functools import cache
from pathlib import Path

from joblib import Memory
from lark import Lark, Tree

memory = Memory('./joblib-cache', verbose=False)

REPL_STRS, INPUT_STR = sys.stdin.read().strip().split('\n\n')
_REPLS = [s.split(' => ') for s in REPL_STRS.splitlines()]
REPLS: list[tuple[str, str]] = [(l, r) for l, r in _REPLS]
REV_REPLS = [(r, l) for l, r in REPLS]


def molecules(s: str):
    return re.findall(r'[A-Z][a-z]?', s)


def construct_grammar():
    revs = defaultdict(set)
    exprs = defaultdict(set)

    for l, r in REPLS:
        # revs[l].add(l)
        revs[l].add(r)

    for l, rs in list(revs.items()):
        for r in rs:
            # s = ' '.join(f'"{m}"' for m in molecules(r))
            s = ' '.join(f'{m.lower()}' for m in molecules(r))
            exprs[r].add(s)
            # revs[r].add(f'"{r}"')

    # for m in set(molecules(REPL_STRS)):
    #     revs[m.lower()].add(f'"{m}"')

    grammar = ''
    for r, ss in exprs.items():
        grammar += f'{r.lower()} : {" | ".join(ss)}\n'

    grammar += '\n'
    for l, rs in revs.items():
        grammar += f'{l.lower()} : "{l}" | {" | ".join(rs).lower()}\n'

    grammar += '\n'
    ms = set(molecules(REPL_STRS))
    for m in ms:
        if m not in set(exprs) | set(revs):
            grammar += f'{m.lower()} : "{m}"\n'

    return grammar


def parse_tree(inp: str):
    grammar = construct_grammar()
    parser = Lark(grammar, start="e", ambiguity="explicit")
    print('Parsing...')
    forest = parser.parse(inp)
    return forest


cachefile = Path('cache.pkl')

if not cachefile.exists():
    with open(cachefile, 'wb') as f:
        forest = parse_tree(INPUT_STR)
        pickle.dump(forest, f)
else:
    with open(cachefile, 'rb') as f:
        forest = pickle.load(f)
        assert isinstance(forest, Tree)

# print(tree.pretty())
# print(dir(tree))

# print(tree.data)
# print(tree.children)


@cache
def tree_depth(t):
    if isinstance(t, Tree):
        if not t.children:
            return 1

        cjoin = ''.join(c.data for c in t.children)
        cost = t.data != cjoin
        # print(t.data, cjoin)

        return cost + max(
            tree_depth(child)
            for child in t.children if isinstance(child, Tree)
        )
    else:
        return 1


@cache
def find_shallowest(t):
    if t.data == '_ambig':
        shallowest = min(t.children, key=tree_depth)
        return find_shallowest(shallowest)
    else:
        new_children = [
            find_shallowest(c) if isinstance(c, Tree) else c
            for c in t.children
        ]
        return Tree(t.data, new_children)


maxdepth = float('inf')


def explore(t: Tree, d=0):
    global maxdepth

    if not t.children:
        print(d, t.data)
        maxdepth = min(maxdepth, d)

    for c in t.children:
        if d < maxdepth:
            explore(c, d + 1)


print(forest.data)
for c in forest.children:
    print(c.data)

explore(forest)

exit()

# print('Prettifying...')
# print(forest.pretty())

print('Finding shallowest...')
s = find_shallowest(forest)
print(tree_depth(s) - 1)
