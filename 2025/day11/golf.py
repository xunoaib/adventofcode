import functools as f
o='out'
p=lambda c:[sum(map(p,g[c])),1][c==o]
q=f.cache(lambda c,s:[sum(q(n,s|(n=='fft')|(n=='dac')*2)for n in g[c]),s>2][c==o])
g={a[:-1]:b for a,*b in map(str.split,open(0))}|{o:[]}
print(p('you'),q('svr',0))