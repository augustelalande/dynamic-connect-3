import math

from utils.interface import action_string
from utils.state import get_actions, is_winning
from utils.runs import num_runs

action_mappings = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}

class SmartAgent(object):

    def __init__(self, color=0): # white=0 black=1
        self.white = [(1, 1), (1, 3), (5, 2), (5, 4)] # white pieces
        self.black = [(1, 2), (1, 4), (5, 1), (5, 3)] # black pieces
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

    def take_action(self, search_depth=7):
        actions = get_actions(self.pieces, self.opponent)
        action_vals = [self.alphabeta_search(a, search_depth-1, float("-inf"), float("inf")) for a in actions]
        print([action_string(self.pieces[a[0]], a[1]) for a in actions])
        print(action_vals)
        if self.color == 0:
            best_value = max(action_vals)
        else:
            best_value = min(action_vals)
        best_action = actions[action_vals.index(best_value)]
        action = action_string(self.pieces[best_action[0]], best_action[1])
        self.pieces[best_action[0]] = best_action[1]
        self.playing = 1 if self.color == 0 else 0
        return action

    def alphabeta_search(self, action, depth, alpha, beta):
        if self.playing == 0:
            self.playing = 1
            tmp_cell = self.white[action[0]]
            self.white[action[0]] = action[1]
        else:
            self.playing = 0
            tmp_cell = self.black[action[0]]
            self.black[action[0]] = action[1]

        if self.playing == 1 and is_winning(self.white, self.black):
            h = 1000 + depth
        elif self.playing == 0 and is_winning(self.black, self.white):
            h = -1000 - depth
        elif depth == 0:
            h = self.heuristic()
        else:
            if self.playing == 0:
                h = float("-inf")
                for a in get_actions(self.white, self.black):
                    h = max(h, self.alphabeta_search(a, depth-1, alpha, beta))
                    alpha = max(alpha, h)
                    if beta <= alpha: break
            else:
                h = float("inf")
                for a in get_actions(self.black, self.white):
                    h = min(h, self.alphabeta_search(a, depth-1, alpha, beta))
                    beta = min(beta, h)
                    if beta <= alpha: break

        if self.playing == 0:
            self.playing = 1
            self.black[action[0]] = tmp_cell
        else:
            self.playing = 0
            self.white[action[0]] = tmp_cell
        return h

    def heuristic(self):
        white2runs = num_runs(self.white, 2)
        black2runs = num_runs(self.black, 2)
        position_score = 0
        if self.color == 0:
            for c in self.white:
                position_score += cell_score(c) / 10
        else:
            for c in self.black:
                position_score -= cell_score(c) / 10
        return position_score + white2runs - black2runs

def cell_score(c, n=5, m=4): # give score to cell based on distance from edge
    xscore = min(c[0] - 1, n - c[0])
    yscore = min(c[1] - 1, m - c[1])
    return math.sqrt(xscore * xscore + yscore * yscore)

# for i in range(1,5):
#     for j in range(1,6):
#         print(cell_score((j, i)), end=" ")
#         # print(j, i)
#     print()