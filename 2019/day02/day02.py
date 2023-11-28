#!/usr/bin/env python
import sys

def run_simulation(vals, val1, val2):
    vals[1] = val1
    vals[2] = val2
    try:
        pc = 0
        while pc < len(vals):
            opcode = vals[pc]
            ind1, ind2, ind3 = vals[pc+1:pc+4]
            if opcode == 1:
                vals[ind3] = vals[ind1] + vals[ind2]
            elif opcode == 2:
                vals[ind3] = vals[ind1] * vals[ind2]
            elif opcode == 99:
                break
            pc += 4

    except IndexError:
        print('computer caught fire')
    finally:
        # print(','.join(map(str, vals)))
        return vals[0]

vals = list(map(int, sys.stdin.read().split(',')))

# part 1
# res = run_simulation(vals, 12, 2)
# print(res)

# part 2
for noun in range(100):
    for verb in range(100):
        res = run_simulation(vals.copy(), noun, verb)
        if res == 19690720:
            print(f'100 * {noun} + {verb} =', 100*noun+verb)
