#!/usr/bin/env python3

import pickle
import time

nums = map(int, input())

num_files = 0
blocks = []
items = []

for i, size in enumerate(nums):
    isfile = not (i % 2)
    if isfile:
        for _ in range(size):
            blocks.append(num_files)
        items.append(('file', size, num_files))
        num_files += 1
    else:
        for _ in range(size):
            blocks.append('.')
        items.append(('.', size, None))

i = 0
j = len(blocks) - 1
while True:
    while blocks[i] != '.':
        i += 1
    while blocks[j] == '.':
        j -= 1
    if i >= j:
        break
    blocks[i], blocks[j] = blocks[j], blocks[i]
a1 = sum(i * int(n) for i, n in enumerate(blocks) if n != '.')
print('part1:', a1)

def disp():
    lst = []
    for a,b,c in items:
        if a == '.':
            lst.append('.'*b)
        else:
            lst += [c] * b
    # print(lst)
    ans = '|'.join(map(str, lst))

    # print(ans)
    # print()

    return ans

def calculate():
    last_time = time.time()
    for file_id in range(num_files)[::-1]:
        try:
            file_idx, file_size = next((idx, item[1]) for idx, item in enumerate(items) if item[0] == 'file' and item[2] == file_id)
            free_idx, free_size = next((idx, item[1]) for idx, item in enumerate(items) if item[0] == '.' and item[1] >= file_size)
        except StopIteration:
            continue

        if file_idx < free_idx:
            continue

        # print(f'moving {file_id} from {file_idx} to {free_idx}')

        items[free_idx] = ('.', free_size - file_size, None)
        items[file_idx] = ('.', file_size, None)
        items.insert(free_idx, ('file', file_size, file_id))

        for idx in range(len(items)-1):
            (t1, s1, id1), (t2, s2, id2) = items[idx:idx+2]
            if t1 == t2 == '.':
                items[idx] = ('.', s1+s2, None)
                del items[idx+1]
                break

        for i in range(len(items))[::-1]:
            if items[i][1] == 0:
                del items[i]

        if time.time() - last_time > 1:
            last_time = time.time()
            print(file_id)

    with open('items.pkl','wb') as f:
        pickle.dump(items, f)

# calculate()
with open('items.pkl','rb') as f:
    items = pickle.load(f)

a2 = 0
pos = 0

for idx, (t, sz, fid) in enumerate(items):
    if t == '.':
        pos += sz
    else:
        for _ in range(sz):
            a2 += pos * fid
            pos += 1

print('part2:', a2)

assert a1 == 6360094256423
assert a2 == 6379677752410
