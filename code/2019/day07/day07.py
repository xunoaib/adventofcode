#!/usr/bin/env python
# overly-complex, messy, and unoptimized... BUT functional
import queue
import sys
import threading
from itertools import permutations

class Amp:
    def __init__(self, prog, inputs, outputs):
        self.prog = prog.copy()
        self.inputs = inputs
        self.outputs = outputs

    def run(self):
        return run_to_halt(self.prog, self.inputs, self.outputs)

def run_to_halt(prog, inputs, outputs=None):
    """Run intcode computer until it halts, returning the last outputted value.
    :param inputs: List or synchronized Queue of input values. Expects phase as the first input.
    :param outputs: List or synchronized Queue to put/append generated output to.
    """
    pc = 0
    last_output = None
    while pc < len(prog):
        opcode = prog[pc]

        # parameter modes (immediate vs position)
        mode1, mode2, mode3 = 0,0,0  # mode 'a' is unused
        if opcode >= 100:
            mode3 = opcode // 10**4
            mode2 = (opcode % 10**4) // 10**3
            mode1 = (opcode % 10**3) // 10**2
            opcode %= 100
        assert mode3 == 0

        if opcode == 99:
            return last_output

        ind1 = prog[pc+1]
        val1 = ind1 if mode1 else prog[ind1]

        if opcode == 3:
            if isinstance(inputs, queue.Queue):
                prog[ind1] = inputs.get()
                inputs.task_done()
            else:
                prog[ind1] = inputs.pop(0)
            pc += 2
            continue

        if opcode == 4:
            last_output = val1
            if outputs is not None:
                outputs.put(last_output)
            pc += 2
            continue

        ind2 = prog[pc+2]
        val2 = ind2 if mode2 else prog[ind2]

        if opcode == 5:  # if v1 != 0, pc = v2 (jump if true)
            pc = val2 if val1 != 0 else pc + 3
            continue

        if opcode == 6:  # if v1 == 0, pc = v2 (jump if false)
            pc = val2 if val1 == 0 else pc + 3
            continue

        ind3 = prog[pc+3]

        if opcode == 1:
            prog[ind3] = val1 + val2
            pc += 4
        elif opcode == 2:
            prog[ind3] = val1 * val2
            pc += 4
        elif opcode == 7:  # if v1 < v2, vals[ind3] = 1, else 0 (less than)
            prog[ind3] = int(val1 < val2)
            pc += 4
        elif opcode == 8:  # if v1 == v2, vals[ind3] = 1, else 0 (equals)
            prog[ind3] = int(val1 == val2)
            pc += 4
        else:
            raise ValueError(f'unknown opcode: {opcode}')

def part1_thrust(prog: list, phases: list, start_val=0):
    """Calculate thrust for part 1 given the intcode and phase settings for each amplifier"""
    for phase in phases:
        start_val = run_to_halt(prog.copy(), [phase, start_val])
    return start_val

def part2_thrust(prog: list, phases: list, start_val=0):
    """Calculate thrust for part 2 given the intcode and phase settings for each amplifier (using threads).
    Input and output between intcode computers is done using a producer/consumer model.
    """
    queues = [queue.Queue() for _ in phases]
    amps, threads = [], []
    for i, phase in enumerate(phases):
        inputs = queues[i]
        outputs = queues[(i+1) % len(phases)]  # output to the next amp's input
        inputs.put(phase)  # send phase setting as input

        amp = Amp(prog, inputs, outputs)
        t = threading.Thread(target=amp.run, daemon=True)
        t.start()

        threads.append(t)
        amps.append(amp)

    queues[0].put(start_val)  # start process by sending signal 0 as input to amplifier A

    for t in threads:
        t.join()

    # return last output from the last amplifier (E), aka next input value of A
    assert sum(q.qsize() for q in queues) == 1
    return queues[0].get()

def solve(func, prog, phases, start_val=0):
    """Test every permutation of the given phase settings to generate the maximum possible thrust.
    :param func: thrust calculation function (part1 vs part2)
    """
    values = set()
    for perm in permutations(phases):
        thrust = func(prog, perm, start_val)
        values.add(thrust)
    return max(values)

def part1(prog, phases):
    return solve(part1_thrust, prog, phases)

def part2(prog, phases):
    return solve(part2_thrust, prog, phases)

def main():
    prog = list(map(int, sys.stdin.read().split(',')))

    ans1 = part1(prog, phases=[0,1,2,3,4])
    print('part1:', ans1)

    ans2 = part2(prog, phases=[5,6,7,8,9])
    print('part2:', ans2)

    assert ans1 == 298586
    assert ans2 == 9246095

if __name__ == '__main__':
    main()
