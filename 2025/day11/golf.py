from functools import cache
o='out'
p=lambda c:[sum(map(p,g[c])),1][c==o]
q=cache(lambda c,s:[sum(q(n,s|(n=='fft')|(n=='dac')*2)for n in g[c]),s>2][c==o])
g={o:[]}
for l in open(0):
	a,*b=l[:-1].split()
	g[a[:-1]]=set(b)
print(p('you'),q('svr',0))