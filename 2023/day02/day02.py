#!/usr/bin/env python3
import re
import sys

GOAL_COUNTS = {'red': 12, 'green': 13, 'blue': 14}
GOAL_TOTALS = sum(GOAL_COUNTS.values())


def valid_round(round):
    return all(count <= GOAL_COUNTS[color] for color, count in round.items())


def main():
    data = sys.stdin.read().strip()

    games = []
    for rounds in re.findall(r'Game \d*: (.*)', data):
        games.append([])
        for cubeset in rounds.split('; '):
            counts = {}
            for item in cubeset.split(', '):
                count, color = item.split(' ')
                counts[color] = int(count)
            games[-1].append(counts)

    ans1 = 0
    for gameid, rounds in enumerate(games, 1):
        if all(map(valid_round, rounds)):
            ans1 += gameid

    ans2 = 0
    for rounds in games:
        mins = {'red': 0, 'green': 0, 'blue': 0}
        for counts in rounds:
            for color, count in counts.items():
                mins[color] = max(count, mins[color])

        v = list(mins.values())
        ans2 += v[0] * v[1] * v[2]

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 2617
    assert ans2 == 59795


if __name__ == '__main__':
    main()
