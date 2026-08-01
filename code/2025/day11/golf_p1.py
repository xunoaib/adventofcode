g={a[:-1]:b for a,*b in map(str.split,open(0))}|{'out':[]}
p=lambda c:c=='out' or sum(map(p,g[c]))
print(p('you'))
