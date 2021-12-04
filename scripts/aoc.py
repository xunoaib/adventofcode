#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys
import time

from aoclib import AOC

def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    group = parser.add_argument_group()
    group.add_argument('challenge', nargs='?', default='.', help='Challenge path/string in the form: 2021/day1. Defaults to the current directory')
    group.add_argument('-c', '--cookiefile', default='cookies.env', help='Path to dotenv file with "cookies" field')

    dl = subparsers.add_parser('download', help='Download sample input based on current directory')
    dl.add_argument('-i', '--interval', type=float, help='Seconds to wait between failed requests')
    dl.add_argument('-o', '--outfile', type=str, nargs='?', const='', help='Output file to write to if successful. Use this option without a value for automatic naming (./dayX.in)')

    subparsers.add_parser('submit', help='Submit answer for last input line matching "part[1-2]: <answer>"')
    subparsers.add_parser('auth', help='Retrieve name of currently logged-in user using cookie (auth check)')
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    aoc = AOC.from_dotenv(args.cookiefile)

    funcs = {
        'submit': lambda args: submit(aoc, args.challenge),
        'download': lambda args: download(aoc, args.challenge, args.interval, args.outfile),
        'auth': lambda args: auth(aoc),
    }

    if func := funcs.get(args.cmd):
        return func(args)

def auth(aoc: AOC):
    if username := aoc.get_username():
        print(f'logged in as {username}')
    else:
        print('not logged in')

def download(aoc: AOC, challenge_path: str, interval: float, outfile: str):
    year, day = AOC.parse_date(challenge_path)

    # infer output filename
    if outfile is None:
        outfile = '/dev/stdout'
    elif outfile == '':
        outfile = f'day{day}.in'

    # prompt to overwrite
    if outfile != '/dev/stdout' and pathlib.Path(outfile).exists():
        if input(f'{outfile} already exists. Overwrite? [y/N] ').lower() != 'y':
            return 1

    print(f'downloading {AOC.URL}/{year}/day/{day}/input to {outfile}')
    while True:
        try:
            sample_input = aoc.get_input(year, day)
            with open(outfile, 'w') as f:
                f.write(sample_input)
            print(f'saved {len(sample_input)} bytes')
            break
        except Exception:
            if interval:
                print(f'download failed. waiting {interval}s...')
                time.sleep(interval)
            else:
                print('download failed')
                break

def submit(aoc, challenge_path):
    year, day = AOC.parse_date(challenge_path)

    # parse level/answer from last line matching "partN: answer"
    level, answer = None, None
    for line in sys.stdin.readlines()[::-1]:
        if m := re.search('^part([1,2]): (.*)$', line):
            level, answer = m.groups()
            break

    if None in (level, answer):
        raise ValueError('Error: no line found matching "part[1-2]: <answer>"')

    # describe submission
    print(f'AoC {year}, Day {day}, Part {level}')
    print('Submitting:', repr(answer))

    message = aoc.submit_answer(year, day, level, answer)
    print(message)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as exc:
        print(exc)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(2)
