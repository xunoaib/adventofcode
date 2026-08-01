import functools as f
g={a[:-1]:b for a,*b in map(str.split,open(0))}|{'out':[]}
q=f.cache(lambda c,s:[sum(q(n,s|(n=='fft')|(n=='dac')*2)for n in g[c]),s>2][c=='out'])
print(q('svr',0))
