import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import override


@dataclass
class Bot:
    id: int
    low: 'Bot | Output | None' = None
    high: 'Bot | Output | None' = None

    @override
    def __repr__(self) -> str:
        l = f'{self.low.__class__.__name__}_{self.low.id}' if self.low else 'None'
        h = f'{self.high.__class__.__name__}_{self.high.id}' if self.high else 'None'
        return f'Bot(id={self.id}, low={l}, high={h})'


@dataclass
class Value:
    val: int
    out: Bot


@dataclass
class Output:
    id: int


def get_bot(id_: int):
    return bots.setdefault(id_, Bot(id_))


def get_output(id_: int):
    return outputs.setdefault(id_, Output(id_))


def lookup_object(spec: str):
    dtype, id = spec.split(' ')
    id = int(id)

    if dtype == 'output':
        return get_output(id)
    elif dtype == 'bot':
        return get_bot(id)
    raise ValueError(f'Unknown spec: {spec}')


lines = sys.stdin.read().splitlines()

val_rules = {}
bot_rules = {}

bots: dict[int, Bot] = {}
outputs: dict[int, Output] = {}

for line in lines:
    if m := re.match(r'^value (.*) goes to bot (.*)$', line):
        val, bid = map(int, m.groups())
        val_rules[val] = bid
    elif m := re.match(r'^bot (.*) gives low to (.*) and high to (.*)$', line):
        bid, low, high = m.groups()
        bid = int(bid)
        bot_rules[bid] = (low, high)

        bot = get_bot(bid)
        bot.low = lookup_object(low)
        bot.high = lookup_object(high)

        print(bot)
