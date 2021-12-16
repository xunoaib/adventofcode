#!/usr/bin/env python3
import math
import operator
import re
import sys
from functools import reduce


class Literal:
    def __init__(self, ver, tid, value):
        self.ver = ver
        self.tid = tid
        self.value = value

    def __repr__(self):
        return f'Literal {self.ver}.{self.tid} = {self.value}'

    def evaluate(self):
        return self.value

class Operator:
    def __init__(self, ver, tid, subpackets):
        self.ver = ver
        self.tid = tid
        self.packets = subpackets

    def __repr__(self):
        return f'Operator {self.ver}.{self.tid} = {self.packets}'

    def evaluate(self):
        vals = [p.evaluate() for p in self.packets]
        if self.tid == 0:
            return sum(vals)
        if self.tid == 1:
            return reduce(operator.mul, vals)
        if self.tid == 2:
            return min(vals)
        if self.tid == 3:
            return max(vals)
        if self.tid == 5:
            return 1 if vals[0] > vals[1] else 0
        if self.tid == 6:
            return 1 if vals[0] < vals[1] else 0
        if self.tid == 7:
            return 1 if vals[0] == vals[1] else 0

class Parser:
    def __init__(self, bb):
        self._bb = bb
        self.idx = 0
        self.ver_total = 0

    def read(self, numbits):
        bits = self._bb[self.idx:self.idx + numbits]
        self.idx += numbits
        return bits

    @property
    def bb(self):
        return self._bb[self.idx:]

    def read_header(self):
        ver = int(self.read(3), 2)
        tid = int(self.read(3), 2)
        self.ver_total += ver
        return ver, tid

    def next_packet(self):
        ver, tid = self.read_header()
        if tid == 4:
            bitsread, value = self.parse_literal()
            packet = Literal(ver, tid, value)
        else:
            bitsread, subpackets = self.parse_operator()
            packet = Operator(ver, tid, subpackets)
        return bitsread + 6, packet

    def parse_literal(self):
        match = re.search('^(.....)*?(0....)', self.bb)
        groups = self.read(match.end())
        groups = re.findall('.....', groups)
        value = int(''.join(g[1:] for g in groups if g), 2)
        return match.end(), value

    def parse_operator(self):
        packets = []
        total_read = 0

        lentid = int(self.read(1))
        if lentid == 0:
            bits_left = int(self.read(15), 2)
            while total_read < bits_left:
                bitsread, packet = self.next_packet()
                packets.append(packet)
                total_read += bitsread
            total_read += 15
        else:
            num_packets = int(self.read(11), 2)
            for i in range(num_packets):
                bitsread, packet = self.next_packet()
                packets.append(packet)
                total_read += bitsread
            total_read += 11
        return total_read + 1, packets

def main():
    data = sys.stdin.read().strip()
    bdata = bin(int(data, 16))[2:]
    bdata = bdata.zfill(math.ceil(len(bdata) / 8) * 8)

    p = Parser(bdata)
    _, packet = p.next_packet()
    print('part1:', p.ver_total)

    ans2 = packet.evaluate()
    print('part2:', ans2)

    assert p.ver_total == 945
    assert ans2 == 10637009915279

if __name__ == '__main__':
    main()
