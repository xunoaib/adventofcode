import re
import sys


def norm(s: str):
    return s.replace(' ', '')


lines = sys.stdin.read().splitlines()

values = {}
outputs = {}

for line in lines:
    if m := re.match(r'^value (.*) goes to (.*)$', line):
        src, tar = map(norm, m.groups())
        values[int(src)] = tar
    elif m := re.match(r'^(.*) gives low to (.*) and high to (.*)$', line):
        src, low, high = map(norm, m.groups())
        outputs[src] = [low, high]

__import__('pprint').pprint(outputs)
__import__('pprint').pprint(values)

# for bot in bots.values():
#     print(f'Bot {bot.id}:')
#     for i in bot.inputs:
#         print('   ', i.source_func())
#     print()

# Part 1 in progress
