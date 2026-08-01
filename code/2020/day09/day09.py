#!/usr/bin/env python
import sys

nums = list(map(int, sys.stdin))
sums = {}
LEN = 25

# calculate the first 25 sums
for idx1, num1 in enumerate(nums[:LEN+1]):
    for idx2, num2 in enumerate(nums[idx1+1:LEN+1], start=idx1+1):
        sums[(idx1,idx2)] = num1 + num2

# part 1 - check for anomalies, then add 25 new sums, remove 25 oldest sums
for cur_idx, target in enumerate(nums[LEN:], start=LEN+1):
    if target not in sums.values():
        print(f'anomaly found at {cur_idx} => {target}')
        break

    for idx in range(cur_idx-LEN, cur_idx-1):
        del sums[(cur_idx-LEN-1, idx)]
        sums[(idx+1, cur_idx)] = nums[idx+1] + target

# part 2 - search for contiguous sums, starting from the largest values and adding upwards
# note: reuses 'target' from above

for idx1 in range(len(nums)-1, 0, -1):
    total = nums[idx1]
    idx2 = idx1 - 1

    while True:
        total += nums[idx2]

        if total > target:
            break # exceeded target

        if total == target:
            vals = nums[idx2:idx1+1]
            print(f'found sum from {idx2} to {idx1} = {sum(vals)}')
            print('min + max:', min(vals)+max(vals))
            break

        idx2 -= 1
