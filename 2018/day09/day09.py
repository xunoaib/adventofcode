import re
from collections import Counter
from time import time

NUM_PLAYERS, LAST_MARBLE = map(int, re.findall(r'\d+', input()))


def solve(last_marble: int):
    scores = Counter()

    player_turn = 1
    circle = [0]
    cur_idx = 0
    marble_num = 1

    last_update = time()
    last_marble_count = 0

    while marble_num < last_marble:

        # ns = ''.join(
        #     [
        #         f' \033[93m{"("+str(v)+")":>4}\033[0m'
        #         if i == cur_idx else f' {v:>4}' for i, v in enumerate(circle)
        #     ][::-1]
        # )
        # print(f'[{player_turn}] {ns}')

        if time() > last_update + 1:
            print(
                marble_num, (marble_num - last_marble_count) /
                (time() - last_update)
            )
            last_update = time()
            last_marble_count = marble_num

        if marble_num % 23 == 0:
            scores[player_turn] += marble_num
            i = (cur_idx + 7) % len(circle)
            scores[player_turn] += circle.pop(i)
            cur_idx = (i - 1) % len(circle)
        else:
            cur_idx = i = (cur_idx - 1) % len(circle)
            circle.insert(i, marble_num)

        marble_num += 1
        player_turn = (player_turn + 1) % NUM_PLAYERS

    return max(scores.values())


a1 = solve(LAST_MARBLE)
a2 = solve(LAST_MARBLE * 100)

print('part1:', a1)
print('part2:', a2)

assert a1 == 373597
