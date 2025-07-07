import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

lines = sorted(sys.stdin.read().strip().splitlines())

guard = None
asleep_since = {}
time_asleep = Counter()
when_asleep = defaultdict(Counter)

for line in lines:
    datestring, message = re.match(r'\[(.*)\] (.*)', line).groups()
    dt = datetime(*map(int, re.split(r'[-: ]', datestring)))

    if 'begins shift' in message:
        guard = int(message.split(' ')[1][1:])
    elif message == 'falls asleep':
        asleep_since[guard] = dt
    elif message == 'wakes up':
        mins = (dt - asleep_since[guard]).total_seconds() / 60
        time_asleep[guard] += int(mins)
        start = asleep_since[guard]
        while start < dt:
            when_asleep[guard][start.minute] += 1
            start += timedelta(minutes=1)

guard = time_asleep.most_common()[0][0]
minute = when_asleep[guard].most_common()[0][0]
a1 = guard * minute
print('part1:', a1)

best = (-1, None, None)
for guard, sleep_times in when_asleep.items():
    best = max(best, (*sleep_times.most_common()[0][::-1], guard))

a2 = best[1] * best[2]
print('part2:', a2)

# assert a1 == 19830
# assert a2 == 43695
