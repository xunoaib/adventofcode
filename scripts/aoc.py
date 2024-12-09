#!/usr/bin/env python3
import argparse
import os
import pathlib
import re
import shutil
import sys
import time
from datetime import datetime

import websocket
from aoclib import AOC
from private_leaderboard import PrivateLeaderboard

# websocket server used to refresh the web browser
WS_REFRESH_URI = "ws://localhost:8765"


def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    group = parser.add_argument_group()
    group.add_argument('challenge', nargs='?', default='.', help='Challenge path/string in the form: 2021/day1. Defaults to the current directory')
    group.add_argument('-c', '--cookiefile', help='Firefox cookies file (sqlite) if using a non-default profile')

    dl = subparsers.add_parser('download', help='Download sample input based on current directory')
    dl.add_argument('-i', '--interval', type=float, help='Seconds to wait between failed requests')
    dl.add_argument('-o', '--outfile', type=str, nargs='?', const='', help='Output file to write to if successful. Use this option without a value for automatic naming (./dayX.in)')

    subparsers.add_parser('submit', help='Submit answer for last input line matching "part[1-2]: <answer>"')
    subparsers.add_parser('auth', help='Retrieve name of currently logged-in user using cookie (auth check)')

    mkdir = subparsers.add_parser('mkdir', help='Create the next non-existent challenge directory, copy code template, and download sample input')
    mkdir.add_argument('-d','--dir-only', help='Only create the directory')

    stats = subparsers.add_parser('stats', help='Retrieve leaderboard stats')
    stats.add_argument('year', nargs='?')

    leaderboard = subparsers.add_parser('pstats', help='Retrieve private leaderboard stats')
    leaderboard.add_argument('code')
    leaderboard.add_argument('year', nargs='?')
    leaderboard.add_argument('-l','--loop', action='store_true')
    leaderboard.add_argument('-e','--events', action='store_true', help='Notify of leaderboard changes')
    leaderboard.add_argument('-t','--times', action='store_true', help='Show completion datetimes')
    return parser

def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    aoc = AOC.from_firefox(args.cookiefile)
    funcs = {
        'submit': lambda args: not submit_and_refresh(aoc, args.challenge),
        'download': lambda args: download(aoc, args.challenge, args.interval, args.outfile),
        'auth': lambda args: auth(aoc),
        'stats': lambda args: aoc.personal_stats(args.year) and 0,  # suppress output
        'pstats': lambda args: handle_private_leaderboard(aoc, args) and 0,  # suppress output
        'mkdir': lambda args: make_next_dir(aoc, args.dir_only),
    }

    if func := funcs.get(args.cmd):
        return func(args)

def auth(aoc: AOC):
    if username := aoc.get_username():
        print(f'logged in as {username}')
        return 0
    else:
        print('not logged in')
        return 1

def make_next_dir(aoc: AOC, dir_only: bool):
    '''
    Creates the next non-existent challenge directory (ie: day02) in the current directory.
    The zero-padding convention (ie: day2 or day02) of the highest existing day will be used (or default: day02)
    '''
    cwd = pathlib.Path().absolute()

    if not re.match(r'^\d{4}$', cwd.name):
        print('Invalid year format for current directory:', cwd.name)
        return 1

    year = int(cwd.name)
    if year < 2015:
        print(f"Invalid year ({year})! Advent of Code doesn't go back that far")
        return 1

    # find the highest existing day number
    if daydirs := list(cwd.glob('day*')):
        lastdaynumstr = max(daydirs).name[3:]
    else:
        lastdaynumstr = '00'
    nextdaynum = int(lastdaynumstr) + 1

    if not (1 <= nextdaynum <= 25):
        print('Invalid day:', nextdaynum)
        return 1

    # infer zero-padding convention
    nextdirname = f'day{nextdaynum:02}' if lastdaynumstr.startswith('0') else f'day{nextdaynum}'
    print('$ mkdir', nextdirname)
    path = pathlib.Path(nextdirname)
    path.mkdir()

    if dir_only:
        return 0

    # copy code template (hardcoded python file)
    source = pathlib.Path(__file__).parent / 'template.py'
    target = path / f'{nextdirname}.py'
    print(f'$ cp {source} {target}')
    shutil.copy(source, target)

    # download sample input
    os.chdir(path)
    print('$ aoc download')
    main(['download', '-o'])

    return 0

def download(aoc: AOC, challenge_path: str, interval: float, outfile: str):
    year, day = AOC.parse_date(challenge_path)
    dirname = pathlib.Path(challenge_path).expanduser().resolve().name

    # infer output filename
    if outfile is None:
        outfile = '/dev/stdout'
    elif outfile == '':
        outfile = f'{dirname}.in'

    # prompt to overwrite
    if outfile != '/dev/stdout' and pathlib.Path(outfile).exists():
        if input(f'{outfile} already exists. Overwrite? [y/N] ').lower() != 'y':
            return 1

    # if day is today, wait until midnight
    target = datetime(year, 12, day)
    today = datetime.now()
    if target > today:
        diff = target - today
        delay = diff.total_seconds()
        print(f'sleeping for {diff}')
        time.sleep(delay)

        # if we're downloading the upcoming challenge, assume an interval of
        # 1 sec for convenience
        if interval is None:
            interval = 1

    print(f'downloading {AOC.URL}/{year}/day/{day}/input to {outfile}')
    while True:
        try:
            sample_input = aoc.get_input(year, day)
            with open(outfile, 'w') as f:
                f.write(sample_input)
            print(f'{len(sample_input)} bytes written')
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
    return "That's the right answer!" in message

def submit_and_refresh(aoc, challenge_path):
    if result := submit(aoc, challenge_path):
        try:
            ws = websocket.create_connection(WS_REFRESH_URI)
            ws.send("refresh")
            print("Refreshing page...")
            ws.close()
        except Exception as e:
            print(f"Failed to refresh the web page: {e}")

    return result

def handle_private_leaderboard(aoc, args):
    if args.year is None:
        args.year = datetime.now().year
    lb = PrivateLeaderboard(aoc)
    if args.times:
        lb.print_times(args.year)
    elif args.events:
        events = lb.loop_differences(args.year, args.code, args.loop)
        print(events)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as exc:
        print(exc)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(2)
