import re
O={}
I={}
T=int
R=re.search
for L in open(0):
	if m:=R('e (.*) g.*o (.*)',L):s,t=m.groups();O[T(s)]=t;I[t]=I.get(t,[])+[T(s)]
	elif m:=R('(.*) g.*o (.*) a.*o (.*)',L):s,l,h=m.groups();O[s]=[l,h];I|={k:I.get(k,[])+[s]for k in[l,h]}
f=lambda V:len(V)>1and all(isinstance(v,T)for v in V)
q=[i for i in I.items()if f(i[1])]
while q:n,v=q.pop();if set(v)=={61,17}:print(n[:4:]);for v,o in zip(sorted(v),O[n]):I[o][I[o].index(n)]=v;q+=[(o,I[o])]*f(I[o])
x=1
for o in'012':x*=I[f'output '+o][0]
print(x)