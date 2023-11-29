#!/usr/bin/env python3
import json
import re
import sys


def remove_reds(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            if v == 'red':
                return obj.clear()
            remove_reds(v)
    elif isinstance(obj, list):
        for v in obj:
            remove_reds(v)

def json_sum(raw_data):
    return sum(map(int, re.findall('-?[0-9]+', raw_data)))

def part2(raw_data):
    d = json.loads(raw_data)
    remove_reds(d)
    return json_sum(json.dumps(d))

def main():
    raw_data = sys.stdin.read()

    ans1 = json_sum(raw_data)
    print('part1:', ans1)

    ans2 = part2(raw_data)
    print('part2:', ans2)

    assert ans1 == 111754
    assert ans2 == 65402

if __name__ == '__main__':
    main()
