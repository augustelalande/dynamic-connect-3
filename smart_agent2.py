import math
from time import sleep, clock
from copy import copy
from threading import Thread

from utils.interface import action_string
from utils.state import get_actions, is_winning
from utils.runs import num_runs, num_diags
from utils.heuristics import *

action_mappings = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}

class SmartAgent(object):

    nodes = {}
    turn = 0

    def __init__(self, color=0, bigboard=0): # white=0 black=1
        if bigboard:
            self.big = True
            self.n = 7
            self.m = 6
            self.white = [(2, 2), (2, 4), (6, 3), (6, 5)]
            self.black = [(2, 3), (2, 5), (6, 2), (6, 4)]
        else:
            self.big = False
            self.n = 5
            self.m = 4
            self.white = [(1, 1), (1, 3), (5, 2), (5, 4)]
            self.black = [(1, 2), (1, 4), (5, 1), (5, 3)]
        self.playing = 0 # color to play
        self.color = color
        self.pieces = self.white if color == 0 else self.black
        self.opponent = self.white if color == 1 else self.black

    def receive_action(self, action):
        action_cell = (int(action[:-1][0]), int(action[:-1][1]))
        action_map = action_mappings[action[-1]]
        action_result = (int(action_cell[0]) + action_map[0],
                         int(action_cell[1]) + action_map[1])
        if self.playing == 0:
            action_cell_index = self.white.index(action_cell)
            self.white[action_cell_index] = action_result
            self.playing = 1
        else:
            action_cell_index = self.black.index(action_cell)
            self.black[action_cell_index] = action_result
            self.playing = 0
        self.turn += 1

    def take_action(self):
        iterative_search = Thread(target=self.iterative_deepening)
        iterative_search.start()
        sleep(9)
        action = action_string(self.pieces[self.best_action[0]], self.best_action[1])
        self.pieces[self.best_action[0]] = self.best_action[1]
        self.playing = 1 if self.color == 0 else 0
        self.turn += 1
        return action

    def iterative_deepening(self, timeout=7, start_depth=4, max_depth=1000):
        start = clock()
        result_score = 0
        search_depth = start_depth
        white = copy(self.white)
        black = copy(self.black)
        playing = self.playing
        while clock() - start < timeout and abs(result_score) < 1000 and search_depth <= max_depth:
            sequence = set()
            self.nodes_searched = 0
            result = self.alphabeta_search(search_depth, white, black, playing,
                                           sequence, max_depth=search_depth)
            if clock() - start < timeout:
                self.best_action = result[-1]
                result_score = result[0]
                print("depth: {}\nnodes searched: {}\nestimated utility: {}\nbest move: {}\n".format(
                        search_depth, self.nodes_searched, result_score,
                        action_string(self.pieces[self.best_action[0]], self.best_action[1])))
                search_depth += 1

    def alphabeta_search(self, depth, white, black, playing, move_sequence,
                         alpha=float('-inf'), beta=float('inf'), max_depth=1000):
        self.nodes_searched += 1
        action = None

        state = (tuple(sorted(white, key=lambda x: x[0] + 10 * x[1])),
                 tuple(sorted(black, key=lambda x: x[0] + 10 * x[1])), playing)

        if state in move_sequence: return 0
        move_sequence.add(state)

        if state in self.nodes and self.nodes[state][2] >= depth and \
                abs(self.nodes[state][0]) < 1000:
            move_sequence.remove(state)
            if depth == max_depth:
                return (self.nodes[state][0], self.nodes[state][1])
            else:
                return self.nodes[state][0]
        if playing == 1 and is_winning(white):
            h = 1000 + depth
        elif playing == 0 and is_winning(black):
            h = -1000 - depth
        elif depth == 0:
            h = self.heuristic(white, black, playing)
        else:
            if not self.big:
                xstart = 1
                ystart = 1
                n = 5
                m = 4
            else:
                if self.turn > 5:
                    xstart = 1
                    ystart = 1
                    n = 7
                    m = 6
                else:
                    xstart = 2
                    ystart = 2
                    n = 6
                    m = 5

            if playing == 0: # maximizer
                h = float("-inf")

                for a in get_actions(white, black, n, m, xstart, ystart):
                    modified_cell = self.__apply_action(a, white)
                    v = self.alphabeta_search(depth - 1, white, black, 1, move_sequence, alpha, beta)
                    if v > h:
                        h = v
                        action = a
                    self.__undo_action(a, white, modified_cell)

                    # if depth == max_depth:
                    #     print(depth, action_string(white[a[0]], a[1]), v, h)

                    alpha = max(alpha, h) # alpha-beta prunning
                    if beta < alpha: break
            else: # minimizer
                h = float("inf")

                for a in get_actions(black, white, n, m, xstart, ystart):
                    modified_cell = self.__apply_action(a, black)
                    v = self.alphabeta_search(depth - 1, white, black, 0, move_sequence, alpha, beta)
                    if v < h:
                        h = v
                        action = a

                    self.__undo_action(a, black, modified_cell)

                    # if depth == max_depth:
                    #     print(depth, action_string(black[a[0]], a[1]), v)

                    beta = min(beta, h) # alpha-beta prunning
                    if beta < alpha: break

        self.nodes[state] = (h, action, depth)
        move_sequence.remove(state)
        if max_depth == depth:
            return (h, action)
        else:
            return h

    def __apply_action(self, action, cells):
        modified_cell = cells[action[0]]
        cells[action[0]] = action[1]
        return modified_cell

    def __undo_action(self, action, cells, modified_cell):
        cells[action[0]] = modified_cell

    def heuristic(self, white, black, playing):
        h = 0
        h += num_runs(white, 2) # white 2-runs
        h -= num_runs(black, 2) # black 2-runs

        # h += num_diags(white, 2) # white 2-runs
        # h -= num_diags(black, 2) # black 2-runs

        # h += position_score(white, self.n, self.m)
        # h -= position_score(black, self.n, self.m)

        # trapped_white_weight = 10 if self.color == 0 else 5
        # trapped_black_weight = 10 if self.color == 1 else 5
        # h += trapped_pieces(black, white, self.n, self.m)
        # h -= trapped_pieces(white, black, self.n, self.m)

        # h += scored_runs(white, self.n, self.m)
        # h -= scored_runs(black, self.n, self.m)

        # if pattern_check(white): h += 500
        # if pattern_check(black): h -= 500

        # if playing == 0:
        #     if mate_in_1(white, black, self.n, self.m):
        #         h += 900
        #     elif mate_in_2(black, white, self.n, self.m):
        #         h -= 800
        # else:
        #     if mate_in_1(black, white, self.n, self.m):
        #         h -= 900
        #     elif mate_in_2(white, black, self.n, self.m):
        #         h += 800
        return h