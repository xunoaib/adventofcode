import re
import sys

lines = sys.stdin.read().splitlines()

val_rules = {}
bot_rules = {}

for line in lines:
    if m := re.match(r'^value (.*) goes to bot (.*)$', line):
        val, bot = map(int, m.groups())
        val_rules[val] = bot
    elif m := re.match(r'^bot (.*) gives low to (.*) and high to (.*)$', line):
        bot, low, high = m.groups()
        bot_rules[bot] = (low, high)

print(bot_rules)
