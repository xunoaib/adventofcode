#!/usr/bin/env python
import sys
from collections import defaultdict

def run(insts):
    pc, acc = 0, 0
    history = []

    while pc not in history:
        history.append(pc)

        if pc == len(insts):
            print('successful exit')
            break

        op, arg = insts[pc].split(' ')
        arg = int(arg)

        if op == 'jmp':
            pc += arg
            continue
        if op == 'acc':
            acc += arg
        pc += 1
    else:
        print('infinite loop:', pc-arg, '->', pc, f'({op} {arg})')

    print('acc:', acc, 'pc:', pc)
    return history

def find_candidates(insts, history):
    '''Find all nop/jmp instructions that might cause the program to exit cleanly if changed'''
    # create control flow graph from jump instructions
    jmp_graph = {}
    for i, inst in enumerate(insts):
        op, arg = inst.split(' ')
        arg = int(arg)

        if op == 'jmp':
            jmp_graph[i] = i + arg
        else:
            jmp_graph[i] = i + 1

    # for each location, find all locations that jump to it
    jmp_refs = defaultdict(set)
    for src,tar in jmp_graph.items():
        jmp_refs[tar].add(src)

    # find all instructions that eventually lead to program end
    jmp_chain = set()
    frontier = {len(insts)} # start from exit
    while frontier:
        target = frontier.pop()
        jmp_chain.add(target)
        frontier |= jmp_refs[target] - jmp_chain # find all unvisited references

    # only consider changing nops/jmps that were used in the simulation
    used_jmps = [pc for pc in history if 'jmp' in insts[pc]]
    used_nops = [pc for pc in history if 'nop' in insts[pc]]

    # look for any jumps that would flow into the solution chain if nopped
    candidates = []
    for jmp in used_jmps:
        if jmp + 1 in jmp_chain:
            candidates.append(jmp)

    # look for any nops that would jump into the solution chain if jmped
    for nop in used_nops:
        arg = int(insts[nop].split(' ')[1])
        if nop + arg in jmp_chain:
            candidates.append(nop)

    return candidates

# part 1
insts = sys.stdin.read().strip().split('\n')
history = run(insts)

# part 2
if candidates := find_candidates(insts, history):
    print('\nfound jmp/nop candidates:', candidates)
    pc = candidates[0]
    inst = insts[pc]
    if 'jmp' in inst:
        insts[pc] = inst.replace('jmp', 'nop')
    else:
        insts[pc] = inst.replace('nop', 'jmp')

    print(f'changed {inst} to {insts[pc]} at {pc}\n')
    run(insts)
