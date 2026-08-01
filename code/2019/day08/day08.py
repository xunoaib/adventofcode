#!/usr/bin/env python3
import sys

def part1(layers, width=25, height=6):
    counts = [(layer.count(0), layer) for idx, layer in enumerate(layers)]
    count, layer = min(counts)
    return layer.count(1) * layer.count(2)

def part2(layers, width=25, height=6):
    img = layers[0].copy()
    for idx, px in enumerate(img):
        for layer_idx in range(len(layers)):
            if (px := layers[layer_idx][idx]) != 2:
                img[idx] = px
                break

    for row in [img[i:i+width] for i in range(0, len(img), width)]:
        print(''.join('\u2588' if px else ' ' for px in row))

def main():
    pixels = list(map(int, sys.stdin.read().strip()))
    width, height = 25, 6
    # width, height = 2, 2
    layers = [pixels[i:i+width*height] for i in range(0, len(pixels), width*height)]
    assert len(set(map(len, layers))) == 1

    ans1 = part1(layers, width, height)
    print('part1:', ans1)

    ans2 = part2(layers, width, height)
    # print('part2:', ans2)

    assert ans1 == 2125
    # assert ans2 == 0

if __name__ == '__main__':
    main()
