#!/usr/bin/env python3

# NOTE: This code is oriented towards Part 2, and solves it very slowly

import random
import re
import sys
from collections import defaultdict
from heapq import heappop, heappush
from time import time

# state = ('.......', 'AAAA', 'BBBB', 'CCCC', 'DDDD')

ROOM_SIZE = 4
move_costs = dict(zip('ABCD', [1, 10, 100, 1000]))


def inhallway(pos: int):
    return 0 <= pos <= 6


def create_links():
    global links
    links = defaultdict(dict)

    # link hallways
    link(0, 1, 1)
    link(5, 6, 1)
    for h in range(1, 5):
        link(h, h + 1, 2)

    for r in range(4):
        rstart = r * ROOM_SIZE + 7

        # link rooms to hallways
        link(rstart, r + 1, 2)
        link(rstart, r + 2, 2)

        # link inner rooms
        for i in range(3):
            link(rstart + i, rstart + i + 1, 1)


def link(src, tar, cost):
    global links
    links[src][tar] = cost
    links[tar][src] = cost


create_links()


class Game:

    def __init__(self, signature):
        self.board = dict(enumerate(signature))

    @classmethod
    def create_graph(cls, roomsize=4):
        cls.links = {}
        cls.link(0, 1, cost=1)
        cls.link(5, 6, cost=1)

        # link hallways
        for c in range(1, 5):
            cls.link(c, c + 1, cost=2)

        # link homes
        for room in range(4):
            entry = room + 7
            cls.link(entry, room + 1, 2)  # link home to hallways
            cls.link(entry, room + 2, 2)

            # link homes together
            for r in range(1, roomsize):
                # lower = room + 11
                # cls.link(upper, lower, 1)
                prev = entry + (r - 1) * 4
                next = entry + r * 4
                cls.link(prev, next, 1)

        # collect list of nodes accessible from each
        g = defaultdict(set)
        for a, b in cls.links:
            g[a].add(b)
            g[b].add(a)
        cls.connections = dict(g)

    @classmethod
    def find_shortest_bfs(cls, node):
        dist = {node: 0}
        q = [(0, node)]
        while q:
            ucost, u = heappop(q)
            for v in cls.connections[u]:
                alt = ucost + cls.links[(u, v)]
                if alt < dist.get(v, sys.maxsize):
                    dist[v] = alt
                    heappush(q, (alt, v))
        return dist

    @classmethod
    def find_shortest_bfs_all(cls):
        cls.shortest = defaultdict(
            dict)  # shortest distance between any two nodes
        for src in cls.connections:
            for tar, moves in cls.find_shortest_bfs(src).items():
                cls.shortest[src][tar] = moves
                cls.shortest[tar][src] = moves

    @classmethod
    def link(cls, a, b, cost):
        cls.links[(a, b)] = cost
        cls.links[(b, a)] = cost

    def get_all_moves(self):
        '''Get all possible moves, enforcing constraints'''
        for src, tar, cost in self.get_all_moves_unfiltered():
            # Avoid moving within hallway
            if inhallway(src) and inhallway(tar):
                continue
            # Avoid moving within room
            if not inhallway(src) and not inhallway(tar) and get_room(
                    src) == get_room(tar):
                continue
            yield src, tar, cost

    def get_all_moves_unfiltered(self):
        '''Get all technically possible moves without enforcing constraints'''
        for src, tile in self.board.items():
            if tile != '.':
                for tar, cost in self.get_all_moves_from_pos_unfiltered(src):
                    yield src, tar, cost

    def get_all_moves_from_pos_unfiltered(self, src):
        '''Get all available moves (not just adjacent ones) from the current position'''
        q = [(0, src, Game(self.signature()))]
        visited = {src}
        moves = []

        while q:
            tot_cost, src, game = heappop(q)
            for tar, new_cost in game.get_adjacent_moves_from_pos(src):
                if tar not in visited:
                    new_tot_cost = tot_cost + new_cost
                    newgame = game.move_new(src, tar)
                    heappush(q, (new_tot_cost, tar, newgame))
                    moves.append((tar, new_tot_cost))
                    visited.add(tar)

        return moves

    def get_adjacent_moves(self):
        for src, tile in self.board.items():
            if tile != '.':
                for tar, cost in self.get_adjacent_moves_from_pos(src):
                    yield src, tar, cost

    def get_adjacent_moves_from_pos(self, src) -> list[tuple[int, int]]:
        """Get available adjacent moves and their costs from the current pod's position"""
        pod = self.board[src]
        moves = []
        for tar in self.connections[src]:
            # check if target is free
            if self.board[tar] != '.':
                continue

            # # prevent moving from hallway to hallway
            # if 0 <= src <= 6 and 0 <= tar <= 6:
            #     continue

            # enforce rules when moving in room
            if tar >= 7:
                correct_room = (tar - 7) % 4 == 'ABCD'.index(pod)
                moving_inwards = tar > src

                # prevent incorrect creatures from moving inwards
                if moving_inwards and not correct_room:
                    continue

                # prevent moving into room until all unwanted visitors have left
                if moving_inwards and correct_room:
                    res = self.get_residents(tar)
                    if set(res) - {pod, '.'}:
                        continue

            cost = self.links[(src, tar)] * move_costs[pod]
            moves.append((tar, cost))
        return moves

    def get_residents(self, room):
        pos = (room - 7) % 4 + 7  # find room nearest hallway
        tiles = ''
        while tile := self.board.get(pos, None):
            tiles += tile
            pos += 4
        return tiles

    def move(self, src, tar):
        self.board[src], self.board[tar] = self.board[tar], self.board[src]

    def move_new(self, src, tar):
        game = Game(self.signature())
        game.move(src, tar)
        return game

    def signature(self):
        return ''.join(ch for _, ch in sorted(self.board.items()))

    def solved(self):
        return self.signature().endswith('ABCD' * 4)

    def cost_to_solve(self):
        """Estimate the total minimum energy to solve the puzzle, ex: h(x)"""
        # identify target room locations
        targets = defaultdict(set)
        for i, ch in enumerate('ABCD'):
            for m in range(4):  # 4 rows
                targets[ch].add(7 + i + m * 4)

        # group pod positions by letter
        pods = defaultdict(set)  # pods['A'] = [posA1, posA2, ...]
        for pos, ch in self.board.items():
            if ch != '.':
                pods[ch].add(pos)

        # ignore letters already in the correct room
        # unsolved = defaultdict(set)
        total_cost = 0
        for ch in 'ABCD':
            overlap = targets[ch] & pods[ch]
            targets[ch] -= overlap
            pods[ch] -= overlap
            for src, tar in zip(pods[ch], targets[ch]):
                cost = self.shortest[src][tar] * move_costs[ch]
                total_cost += cost
                # print(f'cost {src} -> {tar} = {cost}')
        return total_cost

    def visualize(self):
        return '''
#############
#{}{}.{}.{}.{}.{}{}#
###{}#{}#{}#{}###
  #{}#{}#{}#{}#
  #{}#{}#{}#{}#
  #{}#{}#{}#{}#
  #########
'''.format(*self.signature())


def next_states(state):
    game = Game(state)
    states = []
    moves = sorted(game.get_all_moves(), key=lambda v: v[-1])
    for src, tar, cost in moves:
        ng = game.move_new(src, tar)
        states.append((cost, ng.signature()))
    return states


def bfs(state):
    stop_idx = random.randint(1, 13_000)
    stop_idx = 3475
    print(f'Stopping at iteration {stop_idx}')

    game = Game(state)
    q = [(game.cost_to_solve(), 0, state)]
    visited = {state: 0}
    last = time()
    best = (sys.maxsize, state)
    i = 0
    while q:
        f_current, neg_g, state = heappop(q)
        g = -neg_g

        if i == stop_idx:
            game = Game(state)
            print(game.visualize())
            print()
            for m in game.get_all_moves():
                src, tar, cost = m
                s = game.signature()
                print(s[src], s[tar], str(cost).rjust(4), (src, tar))
            print()
        i += 1

        if state.endswith('ABCD' * 4):
            print(state, g, 'solved', file=sys.stderr)
            return state, g

        new_states = list(next_states(state))
        for g_rel, nstate in new_states:
            g_new = g + g_rel
            h = Game(nstate).cost_to_solve()
            f = g_new + h
            entry = (f, -g_new, nstate)
            if nstate not in visited:
                heappush(q, entry)
                visited[nstate] = g_new
            elif g_new < visited.get(nstate, sys.maxsize):
                # print('adding extra')
                heappush(q, entry)
                visited[nstate] = g_new

        if time() - last > 1:
            print(
                f'f: {f_current}, g: {g} q: {len(q)}, visited: {len(visited)}  {state}'
            )
            last = time()

    print(f'no solution after {len(visited)} states')
    # print(frontier, best)


# def state_tup_fromstring(s):
#     return (s[:7],) + tuple(s[i+7::ROOM_SIZE] for i in range(4))
#
# def solved_tup(state):
#     return all(state[i+1].count(ch) == ROOM_SIZE for i, ch in enumerate('ABCD'))

# def state_fromstring(s):
#     return {i: ch for i, ch in enumerate(s) if ch in 'ABCD'}


def state_fromstring(s):
    return s[:7] + ''.join(s[i + 7::ROOM_SIZE] for i in range(4))


def solved(state):
    return state.endswith('AAAABBBBCCCCDDDD')


def find_pods(state):
    return {i: ch for i, ch in enumerate(state) if ch != '.'}


def get_room(pos):
    if pos < 7:
        raise IndexError(f'Invalid room position: {pos}')
    return (pos - 7) // 4


def correct_room(pod, pos):
    return 'ABCD'.index(pod) == get_room(pos)


# def has_strangers(state, pos):
#     roomstart = get_room(pos) + 7
#     return bool(set(state[roomstart:roomstart + 4]) - {'.', 'ABCD'[room]})


def is_room(pos):
    return pos > 6


# def next_states_pos(state, pos):
#     pod = state[pos]
#
#     if pos < 7:  # in hallway
#         pass
#     elif correct_room(pod, pos):  # in correct room
#         if not has_strangers(state,
#                              pos):  # in correct romom, no further moves needed
#             return []
#     else:  # in incorrect room
#         pass

# def accessible(state, pos):
#     """Find all positions accessible from the current one"""
#     pod = state[pos]
#     assert pod != '.'
#
#     targets = []
#     visited = set()
#     frontier = [(0, pos)]
#     while frontier:
#         cost, pos = heappop(frontier)
#         visited.add(pos)
#
#         for neighbor, addcost in links[pos].items():
#             if neighbor in visited:
#                 continue
#
#             # prevent moving within hallway
#             if 0 <= pos <= 6 and 0 <= neighbor <= 6:
#                 continue
#
#             # enforce blocking rules
#             if state[neighbor] != '.':
#                 continue
#
#             entry = (cost + addcost * move_costs[pod], neighbor)
#
#             # moving into room
#             if is_room(neighbor):
#                 # skip adding suboptimal moves (like moving 'B' @ 10 to 7-9)
#                 # only allow moving into hallway
#                 # todo: move all the way into target room
#                 if correct_room(pod, pos):
#                     targets.append(entry)
#                 # else: incorrect target room. skip adding a target, but add to
#                 # frontier in case a hallway target is open
#
#             # moving into hallway
#             else:
#                 targets.append(entry)
#
#             heappush(frontier, entry)
#             visited.add(neighbor)
#     return targets

# def room_to_hallway(state):
#     """Find moves from each room to the hallway"""
#     for r in range(4):
#         if tup := next((i, ch for ch in enumerate(s[7+r*ROOM_SIZE:]) if ch != '.'), None):
#             pass


def main():
    Game.create_graph()
    Game.find_shortest_bfs_all()

    data = sys.stdin.read()
    sig = re.findall(r'[A-Z\.]', data)

    # solved_sig = '.......ABCDABCDABCDABCD'

    # g = Game(solved_sig)
    # print(g.visualize())
    # print(list(g.get_moves()))
    # print(g.cost_to_solve())
    # return

    # remove hallway tiles immediately outside rooms
    for i in [8, 6, 4, 2]:
        sig = sig[:i] + sig[i + 1:]
    sig = ''.join(sig)

    g = Game(sig)
    print(g.visualize())

    for m in g.get_all_moves():
        src, tar, cost = m
        s = g.signature()
        print(s[src], s[tar], str(cost).rjust(4), (src, tar))

    bfs(g.signature())
    return

    # assert ans1 == 15237
    # assert ans2 == 47509


if __name__ == '__main__':
    main()
