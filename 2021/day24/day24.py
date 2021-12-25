#!/usr/bin/env python3
import re
import sys
from collections import Counter

from z3 import If, BitVec, BitVecVal, Optimize

zero, one = BitVecVal(0, 64), BitVecVal(1, 64)

class ALUClone:
    def __init__(self):
        self.varcount = Counter()  # identifier suffix (for x0, x1, etc)
        self.zvars = {}   # z3 variables: {'x1': BitVec('x1', 64)}
        self.zrules = []  # z3 conditions

        for var in 'wxyz':
            name = f'{var}0'
            self.varcount[var] = 0
            self.zvars[name] = zero

    def exec(self, inst):
        inst = inst.strip()
        if inst.startswith('inp'):
            self.varcount['w'] += 1
            w_id = 'w' + str(self.varcount['w'])
            self.zvars[w_id] = BitVec(w_id, 64)
            return

        op, a_id, b_id = inst.strip().split(' ')

        a_count = self.varcount[a_id]  # retrieve current var number for 'a'
        a_id_new = a_id + str(a_count + 1)  # create identifier for new z3 var
        self.varcount[a_id] += 1  # ... and increment counter
        a_id += str(a_count)  # change 'a' to 'a1'

        a_zvar = self.zvars[a_id]  # retrieve current z3 variable for 'a'
        a_zvar_new = BitVec(a_id_new, 64)  # create new z3 variable
        self.zvars[a_id_new] = a_zvar_new  # ... and save it

        # parse literal value / z3 variable
        if re.match('-?[0-9]+', b_id):
            b_id = int(b_id)
            b_zvar = b_id
        else:
            b_id += str(self.varcount[b_id])
            b_zvar = self.zvars[b_id]  # lookup z3 object for b

        if op == 'add':
            self.zrules.append(a_zvar_new == a_zvar + b_zvar)
        elif op == 'mul':
            self.zrules.append(a_zvar_new == a_zvar * b_zvar)
        elif op == 'div':
            self.zrules.append(a_zvar_new == a_zvar / b_zvar)
            self.zrules.append(b_zvar != 0)
        elif op == 'mod':
            self.zrules.append(a_zvar_new == a_zvar % b_zvar)
            self.zrules.append(a_zvar >= 0)
            self.zrules.append(b_zvar > 0)
        elif op == 'eql':
            self.zrules.append(a_zvar_new == If(a_zvar == b_zvar, one, zero))
        else:
            sys.exit('unknown instruction:', inst)

    def solve(self):
        solver = Optimize()
        solver.add(self.zrules)

        # successful output condition
        z = self.zvars['z' + str(self.varcount['z'])]
        solver.add(z == 0)

        # constrain inputs to single digits
        ws = [self.zvars[f'w{wnum}'] for wnum in range(1, self.varcount['w'] + 1)]
        for w in ws:
            solver.add(w >= 1, w <= 9)

        # maximize/minimize the sum of digits
        for p, func in enumerate((solver.maximize, solver.minimize)):
            solver.push()
            func(sum(w * (10**i) * w for i, w in enumerate(ws[::-1])))
            if solver.check():
                m = solver.model()
                ans = int(''.join(str(m[d]) for d in ws))
                print(f'part{p+1}:', ans)
                yield ans
            solver.pop()

def main():
    insts = sys.stdin.read().strip().splitlines()

    alu = ALUClone()
    for inst in insts:
        alu.exec(inst)

    ans1, ans2 = alu.solve()

    assert ans1 == 97919997299495
    assert ans2 == 51619131181131


if __name__ == '__main__':
    main()
