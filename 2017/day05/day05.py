#!/usr/bin/env python3

def part1(nums):
    idx = 0
    count = 0
    while 0 <= idx < len(nums):
        nums[idx] += 1
        idx += nums[idx] - 1
        count += 1
    return count

def part2(nums):
    idx = 0
    count = 0
    while 0 <= idx < len(nums):
        offset = nums[idx]
        nums[idx] += -1 if offset >= 3 else 1
        idx += offset
        count += 1
    return count

def main():
    with open('day05.in') as f:
        nums = list(map(int, f))

    ans1 = part1(nums.copy())
    ans2 = part2(nums.copy())

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 318883
    assert ans2 == 23948711

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
