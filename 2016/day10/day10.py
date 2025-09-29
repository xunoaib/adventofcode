import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, override


@dataclass
class Bot:
    id: int
    low: 'Bot | Output | None' = None
    high: 'Bot | Output | None' = None
    inputs: list['Source'] = field(default_factory=list)

    @override
    def __repr__(self) -> str:
        l = f'{self.low.__class__.__name__}_{self.low.id}' if self.low else 'None'
        h = f'{self.high.__class__.__name__}_{self.high.id}' if self.high else 'None'
        return f'Bot(id={self.id}, low={l}, high={h})'


@dataclass
class Source:
    source_func: Callable[..., 'Bot']


@dataclass
class Value:
    id: int
    out: Bot


@dataclass
class Output:
    id: int


def get_bot(bid: int):
    return bots.setdefault(bid, Bot(bid))


def get_output(oid: int):
    return outputs.setdefault(oid, Output(oid))


def get_value(vid: int, bid: int | None):
    if bid is None:
        return values[vid]

    bot = get_bot(bid)
    return values.setdefault(vid, Value(vid, bot))


def lookup_object(spec: str):
    dtype, id = spec.split(' ')
    id = int(id)

    if dtype == 'output':
        return get_output(id)
    elif dtype == 'bot':
        return get_bot(id)
    raise ValueError(f'Unknown spec: {spec}')


lines = sys.stdin.read().splitlines()

bots: dict[int, Bot] = {}
outputs: dict[int, Output] = {}
values: dict[int, Value] = {}

for line in lines:
    if m := re.match(r'^value (.*) goes to bot (.*)$', line):
        vid, bid = map(int, m.groups())
        bot = get_bot(bid)
        val = get_value(vid, bid)

        bot.inputs.append(Source(lambda val=val: val.id))

    elif m := re.match(r'^bot (.*) gives low to (.*) and high to (.*)$', line):
        bid, low, high = m.groups()
        bid = int(bid)

        bot = get_bot(bid)
        l = bot.low = lookup_object(low)
        h = bot.high = lookup_object(high)

        if isinstance(l, Bot):
            l.inputs.append(Source(lambda bot=bot: bot.low))
        if isinstance(h, Bot):
            h.inputs.append(Source(lambda bot=bot: bot.high))

for bot in bots.values():
    print(f'Bot {bot.id}:')
    for i in bot.inputs:
        print('   ', i.source_func())
    print()
