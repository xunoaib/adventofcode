import re
from collections import Counter

num_players, last_num = map(int, re.findall(r'\d+', input()))

scores = Counter()

player_turn = 1
circle = [0]
cur_idx = 0
marble_num = 1

while marble_num < last_num:

    # ns = ''.join(
    #     [
    #         f' \033[93m{"("+str(v)+")":>4}\033[0m'
    #         if i == cur_idx else f' {v:>4}' for i, v in enumerate(circle)
    #     ][::-1]
    # )
    # print(f'[{player_turn}] {ns}')

    if marble_num % 23 == 0:
        scores[player_turn] += marble_num
        i = (cur_idx + 7) % len(circle)
        scores[player_turn] += circle.pop(i)
        cur_idx = (i - 1) % len(circle)
    else:
        cur_idx = i = (cur_idx - 1) % len(circle)
        circle.insert(i, marble_num)

    marble_num += 1
    player_turn = (player_turn + 1) % num_players

a1 = max(scores.values())

print('part1:', a1)
