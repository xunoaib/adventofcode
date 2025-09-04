#!/usr/bin/env python
import sys
import re

# cid is optional
fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def check_passport_pt1(passport):
    data = dict([item.split(':') for item in re.split(r'\s', passport)])
    return not bool(set(fields) - set(data.keys()))

def check_passport_pt2(passport):
    data = dict([item.split(':') for item in re.split(r'\s', passport)])
    for key in fields:
        if not (val := data.get(key)):
            return False # missing key
        if not validate_field_pt2(key, val):
            print(f'failed {key} => {val}')
            return False # validation failed
    return not bool(set(fields) - set(data.keys()))

def validate_field_pt2(key, val):
    if key == 'byr':
        return 1920 <= int(val) <= 2002
    elif key == 'iyr':
        return 2010 <= int(val) <= 2020
    elif key == 'eyr':
        return 2020 <= int(val) <= 2030
    elif key == 'hgt':
        if match := re.match(r'^(\d+)cm$', val):
            return 150 <= int(match.group(1)) <= 193
        elif match := re.match(r'^(\d+)in$', val):
            return 59 <= int(match.group(1)) <= 76
        return False
    elif key == 'hcl':
        return bool(re.match('^#[0-9a-f]{6}$', val))
    elif key == 'ecl':
        return val in 'amb blu brn gry grn hzl oth'.split(' ')
    elif key == 'pid':
        return bool(re.match('^[0-9]{9}$', val))
    elif key == 'cid':
        return True
    return False

passports = sys.stdin.read().strip().split('\n\n')
valid = list(map(check_passport_pt2, passports))
print(valid.count(True))
