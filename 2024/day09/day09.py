#!/usr/bin/env python3

import os
import pickle
import time
from dataclasses import dataclass


@dataclass
class File:
    size: int
    id: int

@dataclass
class Free:
    size: int

nums = map(int, input())

num_files = 0
blocks: list[int | str] = []
items: list[File | Free] = []

for i, size in enumerate(nums):
    isfile = not (i % 2)
    if isfile:
        for _ in range(size):
            blocks.append(num_files)
        items.append(File(size, num_files))
        num_files += 1
    else:
        for _ in range(size):
            blocks.append('.')
        items.append(Free(size))

# part 1

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

# part 2

def calculate():
    last_time = time.time()
    for file_id in range(num_files)[::-1]:
        try:
            file_idx, file = next((i,t) for (i,t) in enumerate(items) if isinstance(t, File) and t.id == file_id)
            free_idx, free = next((i,t) for (i,t) in enumerate(items) if isinstance(t, Free) and t.size >= file.size)
        except StopIteration:
            continue

        if file_idx < free_idx:
            continue

        free.size -= file.size
        items[file_idx] = Free(file.size)
        items.insert(free_idx, file)

        for idx in range(len(items)-1):
            a, b = items[idx:idx+2]
            if isinstance(a, Free) and isinstance(b, Free):
                items[idx].size += b.size
                del items[idx+1]
                break

        for i in range(len(items))[::-1]:
            if items[i].size == 0:
                del items[i]

        if time.time() - last_time > 1:
            last_time = time.time()
            print(file_id)

    return items

# cache results to avoid a very slow recalculation
fname = 'items.pkl'
if os.path.isfile(fname):
    items = pickle.load(open(fname, 'rb'))
else:
    items = calculate()
    with open(fname, 'wb') as f:
        pickle.dump(items, f)

a2 = 0
pos = 0

for idx, item in enumerate(items):
    if isinstance(item, File):
        for _ in range(item.size):
            a2 += pos * item.id
            pos += 1
    else:
        pos += item.size

print('part2:', a2)

assert a1 == 6360094256423
assert a2 == 6379677752410
