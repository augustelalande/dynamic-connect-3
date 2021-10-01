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
    """Dynamic connect-3 game playing agent.

        Args:
            color (int): Piece color to be used by this agent. 0 for white, 1 for black.
            bigboard (int, optional): 0 to indicate the use og 5x4 grid, 1 for 7x6 grid.

    """

    nodes = {}
    turn = 0

    def __init__(self, color=0, bigboard=0): # white=0 black=1
        self.big = bigboard
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
        self.playing = 0 # First player is always white
        self.color = color
         # Aliases to facilitate access
        self.pieces = self.white if color == 0 else self.black
        self.opponent = self.white if color == 1 else self.black

    def receive_action(self, action):
        """Update agents game state when opponent plays a move.

        Args:
            action (str): Action played by oppponent. Agent assumes the action is valid without checking.

        """
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
        """Initiates and iterative deepening search to find the optimal move.

        Returns:
            str: Action string of found move.

        """
        iterative_search = Thread(target=self._iterative_deepening)
        iterative_search.start()
        sleep(9)
        action = action_string(self.pieces[self.best_action[0]], self.best_action[1])
        self.pieces[self.best_action[0]] = self.best_action[1]
        self.playing = 1 if self.color == 0 else 0
        self.turn += 1
        return action

    def _iterative_deepening(self, timeout=6, start_depth=4, max_depth=1000):
        start = clock()
        result_score = 0
        search_depth = start_depth
        white = copy(self.white)
        black = copy(self.black)
        playing = self.playing
        while clock() - start < timeout and abs(result_score) < 1000 and search_depth <= max_depth:
            sequence = set()
            self.nodes_searched = 0
            result = self._alphabeta_search(search_depth, white, black, playing,
                                           sequence, max_depth=search_depth,
                                           time_left=timeout - clock() + start)
            if clock() - start < timeout:
                self.best_action = result[-1]
                result_score = result[0]
                print("depth: {}\nnodes searched: {}\nestimated utility: {}\nbest move: {}\n".format(
                        search_depth, self.nodes_searched, result_score,
                        action_string(self.pieces[self.best_action[0]], self.best_action[1])))
                search_depth += 1

    def _alphabeta_search(self, depth, white, black, playing, move_sequence,
                         alpha=float('-inf'), beta=float('inf'), max_depth=1000,
                         time_left=1000):
        """Implementation of depth-limited search using alphabeta prunning.

        This search works by updating the game state with the possible actions at each node and recursively
        descending through the game tree until either a terminal node is reached or the depth goes to zero
        at which point it returns the heuristic value of the game state.

        When comming back up the game tree it undoes the changes it made so that different branches can be explored.

        It also implements alphabeta prunning to stop searching a node once it has established that it will
        never be chosen.

        This search also stores the estimated value at each visited state, the action to take, and the depth
        to which that state has been searched

        This search also tries to branch cycling by returning zero if a state is found which has already been
        seen on the current branch.

        """
        self.nodes_searched += 1 # keep track of nodes searched for displaying
        start_time = clock() # keep track of time to stop the thread
        action = None

        state = (tuple(sorted(white, key=lambda x: x[0] + 10 * x[1])),
                 tuple(sorted(black, key=lambda x: x[0] + 10 * x[1])), playing)

        if state in move_sequence: return 0 # check if state was previously encountered in branch
        move_sequence.add(state)

        # check if node is database of stored nodes at the correct depth
        if state in self.nodes and self.nodes[state][2] >= depth and \
                abs(self.nodes[state][0]) < 1000:
            move_sequence.remove(state)
            if depth == max_depth:
                return (self.nodes[state][0], self.nodes[state][1])
            else:
                return self.nodes[state][0]
        if playing == 1 and is_winning(white): # check that state is not terminal
            val = 100000 + depth
        elif playing == 0 and is_winning(black):
            val = -100000 - depth
        elif depth == 0: # if depth is zero return heuristic approximation
            val = self._heuristic(white, black, playing)
        else:
            if not self.big:
                xstart = 1
                ystart = 1
                n = 5
                m = 4
            else: # this whole set of statements is just to only consider the inner squares
                  # of a big board for the first few moves.
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
                val = float("-inf")

                for a in get_actions(white, black, n, m, xstart, ystart):
                    modified_cell = self._apply_action(a, white)
                    v = self._alphabeta_search(depth - 1, white, black, 1, move_sequence, alpha, beta) # continue searching
                    if v > val: # update value and action if a better path has been found
                        val = v
                        action = a
                    self._undo_action(a, white, modified_cell)

                    alpha = max(alpha, val) # alpha-beta prunning
                    if beta < alpha: break
                    if clock() - start_time > time_left: return # end search if out of time
            else: # minimizer
                val = float("inf")

                for a in get_actions(black, white, n, m, xstart, ystart):
                    modified_cell = self._apply_action(a, black)
                    v = self._alphabeta_search(depth - 1, white, black, 0, move_sequence, alpha, beta)
                    if v < val:# update value and action if a better path has been found
                        val = v
                        action = a

                    self._undo_action(a, black, modified_cell)

                    beta = min(beta, val) # alpha-beta prunning
                    if beta < alpha: break
                    if clock() - start_time > time_left: break # end search if out of time

        self.nodes[state] = (val, action, depth) # update state database
        move_sequence.remove(state)
        if max_depth == depth: # only return the action if at root node
            return (val, action)
        else:
            return val

    def _apply_action(self, action, cells):
        modified_cell = cells[action[0]]
        cells[action[0]] = action[1]
        return modified_cell

    def _undo_action(self, action, cells, modified_cell):
        cells[action[0]] = modified_cell

    def _heuristic(self, white, black, playing):
        h = 0
        h += num_runs(white, 2) # white 2-runs
        h -= num_runs(black, 2) # black 2-runs

        h += num_diags(white, 2) # white 2-runs
        h -= num_diags(black, 2) # black 2-runs

        h += position_score(white, self.n, self.m)
        h -= position_score(black, self.n, self.m)

        h += scored_runs(white, self.n, self.m)
        h -= scored_runs(black, self.n, self.m)

        h -= piece_seperation(white)
        h += piece_seperation(black)

        if playing == 0:
            if mate_in_1(white, black, self.n, self.m):
                h += 900
            elif mate_in_2(black, white, self.n, self.m):
                h -= 800
        else:
            if mate_in_1(black, white, self.n, self.m):
                h -= 900
            elif mate_in_2(white, black, self.n, self.m):
                h += 800
        return h
