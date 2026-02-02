import re
O={}
I={}
for L in open(0):
	if m:=re.search(r'e (.*) g.*o (.*)',L):
		s,t=m.groups()
		O[int(s)]=t
		I[t]=I.get(t,[])+[int(s)]
	elif m:=re.search(r'(.*) g.*o (.*) a.*o (.*)',L):
		s,l,h=m.groups()
		O[s]=[l,h]
		I|={k:I.get(k,[])+[s]for k in[l,h]}

f=lambda V:len(V)>1and all(isinstance(v,int)for v in V)

q=[(n,v)for n,v in I.items()if f(v)]

while q:
	n,v=q.pop()
	for v,o in zip(sorted(v),O[n]):
		I[o][I[o].index(n)]=v
		q+=[(o,I[o])]*f(I[o])

print(a:=next(int(k[4:])for k,v in I.items()if set(v)=={61,17}))
x,y,z=(I[f'output {o}'][0]for o in'012')
print(b:=x*y*z)

assert a == 118
assert b == 143153