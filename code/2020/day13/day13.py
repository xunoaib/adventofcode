#!/usr/bin/env python
import sys

start_time = int(sys.stdin.readline())
values = sys.stdin.readline().strip().split(',')

busses = [(i,int(val)) for i,val in enumerate(values) if val != 'x']
busses.sort(key=lambda tup: tup[1])

# part 1 - use the current time with integer division to find next bus stop times
active = [val for i,val in busses]
nextstops = [((start_time//b)+1)*b for b in active]
nextstop, bus = min(zip(nextstops, active))
print('part1:', bus * (nextstop - start_time))

# part 2
# dumb wolfram alpha solution
# for i,n in busses:
#     print(f'(t + {i}) mod {n} = 0, ', end='')

# find the time at which each new bus becomes staggered with the last.
# the current product of bus ids is the time interval to increase by.
T = 0
intvl = 1
for offset, busid in busses:
    while (T + offset) % busid != 0:
        T += intvl
    intvl *= busid

print('part2:', T)
