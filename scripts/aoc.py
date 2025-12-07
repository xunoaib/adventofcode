#!/usr/bin/env python3
import argparse
import os
import pathlib
import re
import shutil
import sys
import time
from datetime import datetime

import lxml.html
import requests
import websocket
from aoclib import AOC
from private_leaderboard import PrivateLeaderboard

# websocket server used to refresh the web browser
WS_REFRESH_URI = "ws://localhost:8765"


def send_page_refresh(ws_url=WS_REFRESH_URI, verbose=True):
    try:
        if verbose:
            print("\nRefreshing page...")
        ws = websocket.create_connection(ws_url)
        ws.send("refresh")
        ws.close()
    except Exception as e:
        if verbose:
            print(f"Failed to refresh the web page: {e}")


def parse_level_answer_from_output(output: str) -> tuple[int, str]:
    '''
    Parse level (part1 or part2) answer from output. Returns (level, answer).
    Level 1 corresponds to Part 1, etc.
    '''

    # parse level/answer from last line matching "partN: answer"
    level, answer = None, None
    for line in output.split('\n')[::-1]:
        if m := re.search('^part([1,2]): (.*)$', line):
            level, answer = m.groups()
            break

    if None in (level, answer):
        raise ValueError('Error: no line found matching "part[1-2]: <answer>"')

    assert isinstance(level, str)
    assert isinstance(answer, str)
    return int(level), answer


def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    group = parser.add_argument_group()
    group.add_argument(
        'challenge',
        nargs='?',
        default='.',
        help=
        'Challenge path/string in the form: 2021/day1. Defaults to the current directory'
    )
    group.add_argument(
        '-c',
        '--cookiefile',
        help='Firefox cookies file (sqlite) if using a non-default profile'
    )

    dl = subparsers.add_parser(
        'download', help='Download sample input based on current directory'
    )
    dl.add_argument(
        '-i',
        '--interval',
        type=float,
        help='Seconds to wait between failed requests'
    )
    dl.add_argument(
        '-o',
        '--outfile',
        type=str,
        nargs='?',
        const='',
        help=
        'Output file to write to if successful. Use this option without a value for automatic naming (./dayX.in)'
    )

    subparsers.add_parser(
        'submit',
        help='Submit answer for last input line matching "part[1-2]: <answer>"'
    )
    subparsers.add_parser(
        'auth',
        help=
        'Retrieve name of currently logged-in user using cookie (auth check)'
    )

    mkdir = subparsers.add_parser(
        'mkdir',
        help=
        'Create the next non-existent challenge directory, copy code template, and download sample input'
    )
    mkdir.add_argument('-d', '--dir-only', help='Only create the directory')

    stats = subparsers.add_parser('stats', help='Retrieve leaderboard stats')
    stats.add_argument('year', nargs='?')

    leaderboard = subparsers.add_parser(
        'pstats', help='Retrieve private leaderboard stats'
    )
    leaderboard.add_argument('code')
    leaderboard.add_argument('year', nargs='?')
    leaderboard.add_argument('-l', '--loop', action='store_true')
    leaderboard.add_argument(
        '-e',
        '--events',
        action='store_true',
        help='Notify of leaderboard changes'
    )
    leaderboard.add_argument(
        '-t', '--times', action='store_true', help='Show completion datetimes'
    )
    return parser


def parse_stats(html: str) -> dict[int, dict[str, int]]:
    '''
    Parses global stats given HTML from the /<year>/stats page.
    Returns a dict of day: {'part1': int, 'part2': int}
    '''

    tree = lxml.html.fromstring(html)
    results = {}
    for group in tree.xpath('//main/pre[@class="stats"]/a')[::-1]:
        day, part2, part1 = map(int, group.text_content().split()[:3])
        results[day] = {'part1': part1, 'part2': part2}
    return results


from joblib import Memory

memory = Memory('.joblib')


# @memory.cache
def requests_get(url):
    return requests.get(url)


def on_success(year: int, day: int, level: int):
    send_page_refresh(verbose=False)

    # retrieve and print global stats
    assert year >= 2015
    resp = requests_get(f'https://adventofcode.com/{year}/stats')
    results = parse_stats(resp.text)

    part1 = results[day]['part1']
    part2 = results[day]['part2']

    assert level in [1, 2], f'Invalid level: {level}'
    rank = (part1 + part2) if level == 1 else part2

    print()
    print(
        f'\033[93;1mGlobal Solves: \033[93m**\033[0m \033[43;30m {part2} \033[0m / \033[100m {part1} \033[0m \033[90m*\033[0m'
    )
    print()
    bg_color = '\033[43;30m' if level == 2 else '\033[100m'
    rank_str = f'{bg_color} {rank} \033[0m'
    print(
        # f'\033[95;1mYour global rank:\033[0m \033[105;30m {rank} \033[0m \033[95m{"*"*level}\033[0m'
        # f'\033[95;1mYour global rank:\033[0m {rank_str} \033[95m{"*"*level}\033[0m'
        # f'Your global rank:\033[0m {rank_str} {"*"*level}\033[0m'
        # f'Your global rank:\033[0m {rank_str} \033[3m(Day {day}, Part {level})\033[23m'
        f'\033[93mYour global rank:\033[0m {rank_str} / Day {day}, Part {level} {"*"*level}'
    )

    print()


# on_success(2025, 5, level=1)
# on_success(2025, 5, level=2)
# exit()


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    aoc = AOC.from_firefox(args.cookiefile)

    if args.cmd == 'submit':
        print('Reading submission from stdin...', file=sys.stderr)
        output = sys.stdin.read()
        level, answer = parse_level_answer_from_output(output)
        year, day = AOC.parse_date(args.challenge)
        if success := submit(year, day, level, answer, aoc):
            on_success(year, day, level)
        return success

    elif args.cmd == 'download':
        return download(aoc, args.challenge, args.interval, args.outfile)

    elif args.cmd == 'auth':
        return auth(aoc)

    elif args.cmd == 'stats':
        return aoc.personal_stats(args.year) and 0

    elif args.cmd == 'pstats':
        return handle_private_leaderboard(aoc, args) and 0  # suppress output
    elif args.cmd == 'mkdir':
        return make_next_dir(aoc, args.dir_only)
    else:
        print('Unknown command:', args.cmd)
        return 1


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
        print(
            f"Invalid year ({year})! Advent of Code doesn't go back that far"
        )
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
    nextdirname = f'day{nextdaynum:02}' if lastdaynumstr.startswith(
        '0'
    ) else f'day{nextdaynum}'
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
        if input(f'{outfile} already exists. Overwrite? [y/N] '
                 ).lower() != 'y':
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


def submit(year: int, day: int, level: int, answer: str, aoc: AOC):
    assert level in [1, 2]

    # describe submission
    print(f'AoC {year}, Day {day}, Part {level}')
    print('Submitting:', repr(answer))

    message = aoc.submit_answer(year, day, level, answer)
    success = "That's the right answer!" in message

    color = '\033[42;30m' if success else '\033[41;30m'
    print(f'{color}{message}\033[0m')

    return success


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
