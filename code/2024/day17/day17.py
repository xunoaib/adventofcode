#!/usr/bin/env python3

from z3 import BitVecs, Optimize, sat

A,B,C = range(3)
ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = range(8)

r = [int(input().split(': ')[1]) for _ in range(3)]
input()
nums = eval('['+input().split(': ')[1]+']')

def literal(operand):
    return operand

def combo(operand):
    return {
        4: r[A],
        5: r[B],
        6: r[C],
        7: None,
    }.get(operand, operand)

def execute(pc):
    opcode = nums[pc]
    operand = nums[pc+1]

    if opcode == ADV:
        r[A] = r[A] // 2**combo(operand)
    elif opcode == BXL:
        r[B] = r[B] ^ literal(operand)
    elif opcode == BST:
        r[B] = combo(operand) % 8
    elif opcode == JNZ:
        if r[A] != 0:
            pc = literal(operand) - 2
    elif opcode == BXC:
        r[B] = r[B] ^ r[C]
    elif opcode == BXC:
        r[B] = r[B] ^ r[C]
    elif opcode == OUT:
        out.append(combo(operand) % 8)
    elif opcode == BDV:
        r[B] = r[A] // 2**combo(operand)
    elif opcode == CDV:
        r[C] = r[A] // 2**combo(operand)

    return pc + 2

pc = 0
out: list[int] = []
while pc in range(len(nums)):
    pc = execute(pc)

a1 = ','.join(map(str, out))
print('part1:', a1)

def loop(a, b, c):
    b1 = a % 8
    b2 = b1 ^ 1
    c1 = a >> b2
    b3 = b2 ^ 5
    b4 = b3 ^ c1
    a1 = a >> 3
    return a1, b4, c1

s = Optimize()
a, b, c = a0, b0, c0 = BitVecs('a0 b0 c0', 64)
for i in range(len(nums)):
    a,b,c = loop(a, b, c)
    s.add(nums[i] == b % 8)

s.minimize(a0)

assert s.check() == sat

a2 = s.model()[a0].as_long()
print('part2:', a2)

assert a1 == '6,4,6,0,4,5,7,2,7'
assert a2 == 164541160582845
