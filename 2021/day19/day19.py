#!/usr/bin/env python3
from itertools import permutations, product, combinations
import sys


def sub(p1, p2):
    return p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]

def add(p1, p2):
    return p2[0] + p1[0], p2[1] + p1[1], p2[2] + p1[2]

def suball(p1, points):
    return set(sub(p1, p) for p in points)

def addall(p1, points):
    return set(add(p1, p) for p in points)

def mhs(p1, p2):
    return sum(map(abs, sub(p1, p2)))

def relative_vectors(beacons):
    """For each point in a set, generate vectors to all other points"""
    return {b: suball(b, beacons) for b in beacons}

def permute_transforms(beacons):
    """Permute transformations of points by rotating/swapping xyz axes"""
    for idxs in permutations(range(3)):
        for signs in product([-1, 1], [-1, 1], [-1, 1]):
            potential = []
            for pt in beacons:
                rotpt = tuple(pt[idx] * sign for idx, sign in zip(idxs, signs))
                potential.append(rotpt)
            yield potential

def orient(scanners, known_vecs, classified, s2):
    """Attempt to orient scanner s2 relative to an already-oriented scanner"""
    for potential in permute_transforms(scanners[s2]):
        # for each newly-transformed beacon in s2, calculate relative vectors from it
        for b2, rvs2 in relative_vectors(potential).items():
            # look for matching relative vectors among those known to be correctly oriented
            for s1, rvdict1 in known_vecs.items():  # aka: relative_vectors(scanners[s1])
                if s1 == s2:
                    continue
                # check relative vectors from each beacon in s1
                for b1, rvs1 in rvdict1.items():
                    overlap = rvs1 & rvs2
                    if len(overlap) >= 12:  # b1 (in s1) corresponds to b2 (in s2)
                        shift = sub(b2, b1)  # vector transforming b1 to b2 (and all other b's)
                        s2_abs = add(classified[s1], shift)  # absolute position of s2
                        points = set(addall(s2_abs, potential))  # absolute positions of s2 beacons
                        return s2_abs, potential, points

def main():
    groups = sys.stdin.read().strip().split('\n\n')
    scanners = {}
    for group in groups:
        lines = group.split('\n')
        num = int(lines[0].split(' ')[2])
        beacons = []
        for line in lines[1:]:
            point = tuple(map(int, line.split(',')))
            beacons.append(point)
        scanners[num] = beacons

    # relative vectors between correctly-oriented beacons
    known_vecs = {0: relative_vectors(scanners[0])}
    points = {*scanners[0]}  # complete set of absolute beacon positions
    classified = {0: (0, 0, 0)}
    unclassified = set(scanners) - {0}

    while unclassified:
        for s2 in unclassified.copy():
            if result := orient(scanners, known_vecs, classified, s2):
                pos, potential, new_points = result
                print(f'scanner {s2:>2} = {pos}')

                unclassified.remove(s2)
                classified[s2] = pos
                known_vecs[s2] = relative_vectors(potential)
                points |= new_points

    print('part1:', len(points))

    max_dist = 0
    for p1, p2 in combinations(classified.values(), 2):
        dist = mhs(p1, p2)
        if dist > max_dist:
            max_dist = dist
    print('part2:', max_dist)

    assert len(points) == 445
    assert max_dist == 13225


if __name__ == '__main__':
    main()
