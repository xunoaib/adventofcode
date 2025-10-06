from lark import Lark, Tree

grammar = '''
oh : "OH" | o h
ho : "HO" | h o
hh : "HH" | h h

e : "e" | o | h
h : "H" | oh | ho
o : "O" | hh
'''

parser = Lark(grammar, start="e", ambiguity="explicit")

tree = parser.parse('HOH')

# print(tree.pretty())
# print(dir(tree))
# print(tree.data)
# print(tree.children)


def tree_depth(t):
    if isinstance(t, Tree):
        if not t.children:
            return 1
        return 1 + max(
            tree_depth(child)
            for child in t.children if isinstance(child, Tree)
        )
    else:
        return 1


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


for t in tree.children:
    print(tree_depth(t))

print(tree.pretty())

s = find_shallowest(tree)
print(s.pretty())
print(tree_depth(s))
