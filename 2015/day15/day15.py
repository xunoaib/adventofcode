#!/usr/bin/env python3
import re
import sys
from functools import reduce
from itertools import permutations
from operator import mul

import numpy as np


def calc_score(effects, config):
    matrix = [np.array(effects[i], dtype=int) * count for i, count in config.items()]
    matrix = np.stack(matrix)
    sums = np.sum(matrix, axis=0)  # add columns
    return max(reduce(mul, sums), 0)

def best_neighbor(effects, config):
    score = calc_score(effects, config)
    for k1, k2 in permutations(config, 2):
        if config[k2] - 1 < 0:
            continue
        new_conf = config.copy()
        new_conf[k1] += 1
        new_conf[k2] -= 1
        new_score = calc_score(effects, new_conf)
        if new_score > score:
            return new_conf, new_score
    return config, score

def best_calorie_neighbor(effects, config):
    score = calc_score(effects, config)
    for k1, k2 in permutations(config, 2):
        if config[k2] - 1 < 0:
            continue
        new_conf = config.copy()
        new_conf[k1] += effects[k2]  # TODO
        new_conf[k2] -= 1
        new_score = calc_score(effects, new_conf)
        if new_score > score:
            return new_conf, new_score
    return config, score

def main():
    effects = {}
    for line in sys.stdin:
        name, props = line.split(':')
        effects[name] = list(map(int, re.findall('-?[0-9]+', props)))[:-1]

    # initial guess to climb from
    teaspoons = 100
    config = {key: teaspoons // len(effects) for key in effects}

    # everest ho!
    last_score = None
    while True:
        config, score = best_neighbor(effects, config)
        if score == last_score:
            break
        last_score = score

    print(config, score)
    print('part1:', score)

    # ans2 = part2(lines)
    # print('part2:', ans2)

    # assert ans1 == 18965440
    # assert ans2 == 0

if __name__ == '__main__':
    main()
