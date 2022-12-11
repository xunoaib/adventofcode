#!/usr/bin/env python3
import copy
import sys

class Monkey:
    def __init__(self, items, operation, next_monkey_func):
        self.items = items
        self.operation = operation
        self.next_monkey = next_monkey_func
        self.count = 0

    def turn(self, monkies, mod):
        '''
        Processes a single monkey's turn. All items are processed and thrown
        to other monkies. mod is used for part 2 to prevent numbers from exploding.
        '''
        while self.items:
            item = self.items.pop(0)

            if mod:
                worry = self.operation(item) % mod
            else:
                worry = self.operation(item) // 3

            idx = self.next_monkey(worry)
            monkies[idx].items.append(worry)
            self.count += 1

def create_next_monkey_func(divisor, m1, m2):
    '''
    Returns a new function accepting one "worry" argument which returns m1
    or m2 depending on whether that argument is divisible by the divisor.
    '''
    def next_monkey(worry):
        return m1 if worry % divisor == 0 else m2
    return next_monkey

def run_rounds(monkies, rounds, mod):
    monkies = copy.deepcopy(monkies)
    for _ in range(rounds):
        for i, monkey in sorted(monkies.items()):
            monkey.turn(monkies, mod)
    counts = sorted(m.count for m in monkies.values())
    return counts[-1] * counts[-2]

def main():
    groups = sys.stdin.read().strip().split('\n\n')
    monkies = {}

    # part 2 optimization: modulo the worry rating by this maximum divisor to
    # prevent the numbers from becoming huge
    mod = 1

    for monkey_id, group in enumerate(groups):
        lines = group.split('\n')
        items = list(map(int, lines[1].split(': ')[1].split(', ')))
        op = eval('lambda old: ' + lines[2].split('new = ')[1])
        divisor = int(lines[3].split('divisible by ')[1])
        m1 = int(lines[4].split('monkey ')[1])
        m2 = int(lines[5].split('monkey ')[1])
        test = create_next_monkey_func(divisor, m1, m2)
        monkies[monkey_id] = Monkey(items, op, test)
        mod *= divisor

    ans1 = run_rounds(monkies, 20, None)
    ans2 = run_rounds(monkies, 10000, mod)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 54253
    assert ans2 == 13119526120

if __name__ == '__main__':
    main()
