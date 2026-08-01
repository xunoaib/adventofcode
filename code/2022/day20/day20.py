#!/usr/bin/env python3
import sys

# this can be solved a bit more efficiently by only modifying the indices list
# (and not nums), but it's also a bit more confusing to read

def main():
    lines = sys.stdin.read().strip().split('\n')
    nums = list(map(int, lines))
    nums2 = [811589153 * n for n in nums]
    indices = list(range(len(nums)))

    for i in range(len(nums)):
        index = indices.index(i)
        num = nums[index]

        nums = nums[:index] + nums[index+1:]
        indices = indices[:index] + indices[index+1:]

        newpos = (index + num) % len(nums)
        if newpos == 0:
            newpos = len(nums)

        nums.insert(newpos, num)
        indices.insert(newpos, i)

    zeropos = nums.index(0)
    ans1 = 0
    for offset in (1000, 2000, 3000):
        idx = (zeropos + offset) % len(nums)
        ans1 += nums[idx]
    print('part1:', ans1)

    # part 2 is part 1 x 10
    nums = nums2
    indices = list(range(len(nums)))
    for _ in range(10):
        for i in range(len(nums)):
            index = indices.index(i)
            num = nums[index]

            nums = nums[:index] + nums[index+1:]
            indices = indices[:index] + indices[index+1:]

            newpos = (index + num) % len(nums)
            if newpos == 0:
                newpos = len(nums)

            nums.insert(newpos, num)
            indices.insert(newpos, i)

    ans2 = 0
    zeropos = nums.index(0)
    for offset in (1000, 2000, 3000):
        idx = (zeropos + offset) % len(nums)
        ans2 += nums[idx]
    print('part2:', ans2)

    assert ans1 == 8302
    assert ans2 == 656575624777

if __name__ == '__main__':
    main()
