#!/usr/bin/env python
import sys

def run_simulation(vals, input_val):
    vals = vals.copy()
    pc = 0
    last_output = None
    while pc < len(vals):
        opcode = vals[pc]

        # parameter modes (immediate vs position)
        b,c = 0,0  # 'a' is unused
        if opcode >= 100:
            # a = opcode // 10**4
            b = (opcode % 10**4) // 10**3
            c = (opcode % 10**3) // 10**2
            opcode %= 100

        if opcode == 99:
            break

        ind1 = vals[pc+1]
        val1 = ind1 if c else vals[ind1]

        if opcode == 3:
            vals[ind1] = input_val
            pc += 2
            continue

        if opcode == 4:
            last_output = val1
            pc += 2
            continue

        ind2 = vals[pc+2]
        val2 = ind2 if b else vals[ind2]

        if opcode == 5:  # if v1 != 0, pc = v2 (jump if true)
            pc = val2 if val1 != 0 else pc + 3
            continue

        elif opcode == 6:  # if v1 == 0, pc = v2 (jump if false)
            pc = val2 if val1 == 0 else pc + 3
            continue

        ind3 = vals[pc+3]

        if opcode == 7:  # if v1 < v2, vals[ind3] = 1, else 0 (less than)
            vals[ind3] = int(val1 < val2)
            pc += 4
        elif opcode == 8:  # if v1 == v2, vals[ind3] = 1, else 0 (equals)
            vals[ind3] = int(val1 == val2)
            pc += 4
        elif opcode == 1:
            vals[ind3] = val1 + val2
            pc += 4
        elif opcode == 2:
            vals[ind3] = val1 * val2
            pc += 4
        else:
            print('unknown opcode:', opcode)
            return

    return last_output

def main():
    vals = list(map(int, sys.stdin.read().split(',')))

    ans1 = run_simulation(vals, 1)
    print('part1:', ans1)

    ans2 = run_simulation(vals, 5)
    print('part2:', ans2)

    assert ans1 == 5577461
    assert ans2 == 7161591

if __name__ == '__main__':
    main()
