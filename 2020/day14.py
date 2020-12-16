#!/usr/bin/env python
import sys
import parse
from collections import defaultdict

def part1(lines):
    mask_on = 0
    mask_off = 0
    mem = defaultdict(lambda: 0)

    for line in lines:
        line = line.strip()
        if line.startswith('mask'):
            strmask = line.split(' = ')[1][::-1]
            mask_on  = sum(2**i for i,ch in enumerate(strmask) if ch == '1')
            mask_off = sum(2**i for i,ch in enumerate(strmask) if ch != '0')
        else:
            addr, val = parse.parse('mem[{:d}] = {:d}', line)
            memval = (val | mask_on) & mask_off
            mem[addr] = memval

    print('part1:', sum(mem.values()))

def floating_addrs(mask):
    '''Generate addresses by filling in floating bits'''
    # replace each X with a permutation of 0 and 1
    retformat = '0b' + mask.replace('X', '{}')
    fillformat = '{:>0' + str(mask.count('X')) + 'b}'
    for i in range(2 ** mask.count('X')):
        # padding is necessary to generate leading zeroes
        fillvals = fillformat.format(i)
        yield int(retformat.format(*fillvals), 2)

def generate_mask(mask, addr):
    '''Update mask with the appropriate bit rules (part 2)'''
    bits = []
    for i,maskbit in enumerate(mask[::-1]):
        if maskbit == '1':
            bits.append('1')
        elif maskbit == '0':
            addrbit = (addr >> i) & 1
            bits.append(str(addrbit))
        elif maskbit == 'X':
            bits.append('X')
    return ''.join(bits[::-1])

def part2(lines):
    strmask = ''
    mem = defaultdict(lambda: 0)

    for line in lines:
        line = line.strip()
        if line.startswith('mask'):
            strmask = line.split(' = ')[1]
        else:
            addr, val = parse.parse('mem[{:d}] = {:d}', line)
            mask = generate_mask(strmask, addr)
            for newaddr in floating_addrs(mask):
                mem[newaddr] = val
    print('part2:', sum(mem.values()))

lines = sys.stdin.read().strip().split('\n')
part1(lines)
part2(lines)
