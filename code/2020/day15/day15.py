#!/usr/bin/env python

def find_nth(nums, nth):
    # keeps track of the last two times a value was spoken (bad and messy)
    history = {
        n: (i, None) for i,n in enumerate(nums)
    }

    lastspoken = nums[-1]
    lasttuple = history[lastspoken]

    for turn in range(len(nums), nth):
        lastspoken = 0 if None in lasttuple else (lasttuple[0] - lasttuple[1])
        history[lastspoken] = lasttuple = turn, history.get(lastspoken, (None,None))[0]

    print(f'lastspoken: {lastspoken}, turn: {turn+1}')

nums = [11,18,0,20,1,7,16]
find_nth(nums, 2020)
find_nth(nums, 30000000)
