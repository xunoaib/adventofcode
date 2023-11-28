n=int(input());print((lambda b=int((n-1)**.5-1)//2*2+1:(b//2+abs(((n-b**2)-1)%(b+1)-b//2)+1))()if n>1 else 0)
