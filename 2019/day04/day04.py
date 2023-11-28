#!/usr/bin/env python
start, end = 156218, 652527

# TODO: rewrite using and integer instead of a list. this allows for bounds checking

def generate_part1(pwd=None, length=6, minval=0, maxval=10e6):
    pwd = pwd or []
    if len(pwd) >= length:
        num = int(''.join(map(str, pwd)))
        if minval <= num <= maxval:
            # check for double digits
            for i,v in enumerate(pwd[:-1]):
                if v == pwd[i+1]:
                    yield num
                    return
        return

    start = pwd[-1] if pwd else 0
    for d in range(start, 10):
        yield from generate_part1(pwd + [d], length, minval, maxval)

def generate_part2(pwd=None, length=6, minval=0, maxval=10e6):
    pwd = pwd or []
    if len(pwd) >= length:
        num = int(''.join(map(str, pwd)))
        if minval <= num <= maxval and valid_part2(num):
            yield num
        return

    start = pwd[-1] if pwd else 0
    for d in range(start, 10):
        yield from generate_part2(pwd + [d], length, minval, maxval)

# ensure that two consecutive integers exist, not part of a larger group
def valid_part2(num):
    pwd = f'x{num}x'
    for i,v in enumerate(pwd[:-1]):
        if pwd[i-1] != v and pwd[i+1] == v and pwd[i+2] != v:
            return True
    return False

vals = list(generate_part1(minval=start, maxval=end))
print('part1:', len(vals))

vals = list(generate_part2(minval=start, maxval=end))
print('part2:', len(vals))
