a,d=0,50
for l in open(0):d=(d+int(l[1:])*(2*(l[0]<'R')-1))%100;a+=d<1
print(a)