from graphviz import Digraph

g = {a[:-1]: b for a, *b in map(str.split, open(0))}

dot = Digraph(format='png')

for src, targets in g.items():
    dot.node(src)
    for dst in targets:
        dot.edge(src, dst)

dot.render('vis', view=True)
