#!/usr/bin/env python3
import re
import sys


def isvalid(password):
    # skip this check, as generated passwords will not contain iol
    # if re.search('[iol]', password):
    #     return False

    matches = re.findall(r'(.)\1{1,}.*(.)\2{1,}', password)
    if not matches:
        return False

    ascii = list(map(ord, password))
    for i, val in enumerate(ascii[1:-1], 1):
        if ascii[i - 1] < val < ascii[i + 1] and ascii[i + 1] - ascii[i - 1] == 2:
            return True
    return False

def inc_password(password):
    arr = list(password)[::-1]
    i = 0
    while i < len(arr):
        if arr[i] == 'z':
            arr[i] = 'a'
            i += 1
        else:
            arr[i] = chr(ord(arr[i]) + 1)
            if arr[i] in 'iol':  # avoid invalid characters
                continue
            else:
                break
    return ''.join(arr[::-1])

def next_password(password):
    # advance any i/o/l characters forward
    for ch in 'iol':
        password = password.replace(ch, chr(ord(ch) + 1))
    while True:
        password = inc_password(password)
        if isvalid(password):
            return password

def main():
    password = sys.stdin.read().strip()

    ans1 = next_password(password)
    print('part1:', ans1)

    ans2 = next_password(ans1)
    print('part2:', ans2)

    assert ans1 == 'cqjxxyzz'
    assert ans2 == 'cqkaabcc'

if __name__ == '__main__':
    main()
