#!/usr/bin/env python3
import re
import sys
from collections import Counter, defaultdict


def get_dist(elapsed_time, speed, fly_sec, rest_sec):
    num_full, time_left = divmod(elapsed_time, fly_sec + rest_sec)
    if time_left > fly_sec:
        time_left = fly_sec
    return num_full * speed * fly_sec + speed * time_left

def part1(stats):
    return max(get_dist(2503, *item) for item in stats.values())

def part2(stats):
    points = Counter()
    for i in range(1, 2503):
        # group reindeer by distance traveled
        counts = defaultdict(list)
        for name, item in stats.items():
            dist = get_dist(i, *item)
            counts[dist].append(name)

        # award points to the winners
        win_dist, winners = max(counts.items())
        for winner in winners:
            points[winner] += 1
    return max(points.values())

def main():
    lines = sys.stdin.read().strip().split('\n')

    stats = {}
    for line in lines:
        m = re.match('(.*) can fly (.*) km/s for (.*) seconds, but then must rest for (.*) seconds.', line)
        stats[m.group(1)] = tuple(map(int, m.groups()[1:]))

    ans1 = part1(stats)
    print('part1:', ans1)

    ans2 = part2(stats)
    print('part2:', ans2)

    assert ans1 == 2696
    assert ans2 == 1084

if __name__ == '__main__':
    main()
