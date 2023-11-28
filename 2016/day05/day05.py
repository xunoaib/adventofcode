#!/usr/bin/env python3
from hashlib import md5


def main():
    door_id = 'ffykfhsq'

    password1 = ''
    password2 = {}

    idx = 0
    while True:
        data = f'{door_id}{idx}'.encode()
        hash = md5(data).hexdigest()
        idx += 1
        if hash.startswith('0'*5):
            # print(hash, data)

            if len(password1) < 8:
                password1 += hash[5]

            if hash[5] in '01234567' and hash[5] not in password2:
                password2[hash[5]] = hash[6]
                if len(password2) == 8:
                    break

    print('part1:', password1)
    print('part2:', ''.join(kv[1] for kv in sorted(password2.items())))


if __name__ == "__main__":
    main()
