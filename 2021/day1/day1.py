#!/usr/bin/env python3

def main():
    lines = open('day1.in').readlines()
    depths = list(map(int, lines))

    # part 1
    count = 0
    for i in range(1, len(depths)):
        if depths[i-1] < depths[i]:
            count += 1
    print(count)

    # part 2
    sums = []
    for i in range(len(depths)-2):
        sums.append(sum(depths[i:i+3]))

    count = 0
    for i in range(1, len(sums)):
        if sums[i-1] < sums[i]:
            count += 1
    print(count)

if __name__ == "__main__":
    main()
