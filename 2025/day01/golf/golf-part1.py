a,d=0,50
for l in open('x'):r,c=l[0],int(l[1:]);d=(d+c*2*(r<'R')-1)%100;a+=d==0
print(a)