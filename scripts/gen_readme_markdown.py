#!/usr/bin/env python3
import ast
import re
import sys
from dataclasses import dataclass
from functools import cache
from pathlib import Path

TITLES_PATH = Path('titles.json')


@cache
def titles():
    return ast.literal_eval(TITLES_PATH.read_text())


@dataclass
class Day:
    directory: Path

    def __post_init__(self):
        assert self.directory.name.startswith('day')
        assert self.year >= 2015
        assert self.day in range(1, 26)

    @property
    def url(self):
        return f'https://adventofcode.com/{self.year}/day/{self.day}'

    @property
    def solution(self):
        return self.directory / f'day{self.day:02}.py'

    @property
    def year(self):
        return int(self.directory.parent.name)

    @property
    def day(self):
        return int(self.directory.name[3:])

    @property
    def title(self):
        return titles()[self.year][self.day]

    @property
    def solution_rel_to_year(self):
        return self.solution.relative_to(self.directory.parent)

    @property
    def solution_rel_to_root(self):
        return self.solution.relative_to(self.directory.parent.parent)


def parse_days(year_dir: Path):
    return [Day(year_dir / f'day{i:02}') for i in range(1, 26)]


def format_day_row(day: Day):
    title = f'Day {day.day} - {day.title}'
    solution_label = 'Code'
    if day.solution.exists():
        solution = f'[{solution_label}]({day.solution_rel_to_year})'
    else:
        solution = f'{solution_label}'
    return f'| [Day {day.day}: {day.title}]({day.url}) | {solution} |'


def format_days_table(days: list[Day]):
    lines = [
        '|                      Day                      |         Solution       |',
        '| :-------------------------------------------- | :--------------------- |',
    ]
    lines += [format_day_row(day) for day in days]
    return '\n'.join(lines)


def main():
    root = Path(__file__).parent.parent
    year_days = [parse_days(d) for d in sorted(root.glob('20*'))]

    # # Print all solutions relative to root
    # for days in year_days:
    #     year = days[0].year
    #     print(f'# Advent of Code ({year})')
    #     print()
    #     for day in days:
    #         print(
    #             f'- [Day {day.day}: {day.title}]({day.solution_rel_to_root})'
    #         )
    #     print()

    for days in year_days[::-1]:

        year = days[0].year
        year_readme = days[0].solution.parent.parent / 'README.md'
        assert year_readme.exists(), f'Missing {year_readme}'

        rows = [f'# Advent of Code ({year})', '', format_days_table(days), '']
        data = '\n'.join(rows)
        print(data)

        if '-w' in sys.argv:
            with open(year_readme, 'w') as f:
                f.write(data)


if __name__ == '__main__':
    main()
