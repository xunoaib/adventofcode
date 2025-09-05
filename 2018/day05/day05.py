import string


def collapse(s):
    while True:
        l1 = len(s)
        for c in string.ascii_lowercase:
            s = s.replace(f'{c}{c.upper()}', '')
            s = s.replace(f'{c.upper()}{c}', '')
        l2 = len(s)
        if l1 == l2:
            return l2


s = input()

a1 = collapse(s)
print('part1:', a1)

a2 = min(
    collapse(s.replace(c, '').replace(c.upper(), ''))
    for c in string.ascii_lowercase
)
print('part2:', a2)
