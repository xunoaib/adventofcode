import datetime
import pathlib
import re
import requests

import browser_cookie3
from dotenv import dotenv_values, find_dotenv

class AOC:
    PATH_PATTERN = r'(\d{4})/day(\d+)$'  # regex with extraction groups for: (year, month)
    URL = 'https://adventofcode.com'

    def __init__(self, cookies: str):
        self.session = requests.Session()
        self.session.cookies = cookies

    @staticmethod
    def from_dotenv(cookie_file='cookies.env', find=True, usecwd=True):
        ''' Parse HTTP cookies from a dotenv file found in the current or parent directories '''
        if find:
            cookies_env = find_dotenv(cookie_file, usecwd=usecwd)
        cookies = dotenv_values(cookies_env)['cookies']
        return AOC(cookies)

    @staticmethod
    def from_firefox(cookie_file=None):
        # Ex: ~/.mozilla/firefox/xxxxxxxx.default-release/cookies.sqlite
        cookies = browser_cookie3.firefox(cookie_file=cookie_file, domain_name='adventofcode.com')
        return AOC(cookies)

    @classmethod
    def parse_date(cls, path='.'):
        ''' Parse year/day from the given string/path in the form "YYYY/dayN". Returns: year, day'''
        path = pathlib.Path(path).resolve()
        if m := re.search(cls.PATH_PATTERN, str(path)):
            return list(map(int, m.groups()))
        raise ValueError(f'Path error: Expected YYYY/dayN, got: {path}')

    def get_input(self, year, day):
        ''' Download sample input for the given day/year '''
        resp = self.session.get(self.URL + f'/{year}/day/{day}/input')
        if resp.status_code == 200:
            return resp.text
        raise ValueError(f'HTTP Error: {resp.text}')

    def submit_answer(self, year, day, level, answer):
        ''' Submit an answer for the given challenge level (part 1 or 2) '''
        level = int(level)
        if level not in (1, 2):
            raise ValueError(f'Invalid level "{level}", expected 1 or 2')
        resp = self.session.post(self.URL + f'/{year}/day/{day}/answer', data=dict(level=level, answer=answer))

        if match := re.search(r'<main>(.*?)</main>', resp.text, flags=re.DOTALL):
            message = match.group(1)
            message = message.replace('<p>', '<p> ')
            message = re.sub('<.*?>', '', message, flags=re.DOTALL)
            message = re.sub(r'\s{2,}', ' ', message, flags=re.DOTALL)
            return message.strip()
        raise ValueError(f'Unexpected submission response: {repr(resp.text)}')

    def get_username(self):
        ''' Return current username or None if not found '''
        resp = self.session.get(self.URL)
        if m := re.search('<div class="user">(.*?)</div>', resp.text):
            return re.sub(r'<.*?>.*</.*?>', '', m.group(1)).strip()

    def personal_stats(self, year=None, print_stats=True):
        if year is None:
            year = datetime.datetime.now().year

        resp = self.session.get(self.URL + f'/{year}/leaderboard/self')
        if match := re.search(r'<main>.*Score</span>(.*?)</pre>.*?</main>', resp.text, flags=re.DOTALL):
            lines = match.group(1).strip().split('\n')
            results = []
            for line in lines[::-1]:
                result = re.split(r'\s+', line.strip())
                result = [int(v) if v.isnumeric() else v.replace('&gt;', '>') for v in result]
                day, time1, rank1, score1, time2, rank2, score2 = result
                if print_stats:
                    print(f'{day:2}  {time1:>8} {rank1:6}  {time2:>8} {rank2:6}')
                results.append(result)
            return results
