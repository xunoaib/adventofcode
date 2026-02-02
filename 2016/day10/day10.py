import re
O={}
I={}
T=int
R=re.search
for L in open(0):
	if m:=R('e (.*) g.*o (.*)',L):
		s,t=m.groups()
		O[T(s)]=t
		I[t]=I.get(t,[])+[T(s)]
	elif m:=R('(.*) g.*o (.*) a.*o (.*)',L):
		s,l,h=m.groups()
		O[s]=[l,h]
		I|={k:I.get(k,[])+[s]for k in[l,h]}

f=lambda V:len(V)>1and all(isinstance(v,T)for v in V)

q=[(n,v)for n,v in I.items()if f(v)]

while q:
	n,v=q.pop()
	for v,o in zip(sorted(v),O[n]):
		I[o][I[o].index(n)]=v
		q+=[(o,I[o])]*f(I[o])

print(a:=next(T(k[4:])for k,v in I.items()if set(v)=={61,17}))
x,y,z=(I[f'output {o}'][0]for o in'012')
print(b:=x*y*z)

assert a == 118
assert b == 143153