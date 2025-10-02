import re
import sys

repl_strs, input_str = sys.stdin.read().strip().split('\n\n')

repls = [s.split(' => ') for s in repl_strs.splitlines()]

distinct = set()

for srch, repl in repls:
    for i, m in enumerate(re.finditer(srch, input_str)):
        s = input_str[:m.start()] + repl + input_str[m.end():]
        print(s, 'after', srch, repl, 'on', i)
        distinct.add(s)

print('part1:', len(distinct))
