from utils import *

action_mappings = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
inverse_mappings = {(0, -1): 'N', (1, 0): 'E', (0, 1): 'S', (-1, 0): 'W'}

class NaiveAgent(object):

    def __init__(self, state=(('11', '13', '52', '54'), ('12', '14', '51', '53'), 'w'), color='w'):
        self.state = state
        self.color = color

    def receive_action(self, action):
        action_cell = action[:-1]
        action_map = action_mappings[action[-1]]
        action_result = str(int(action_cell[0]) + action_map[0]) + \
                        str(int(action_cell[1]) + action_map[1])
        if self.state[2] == 'w':
            action_cell_index = self.state[0].index(action_cell)
            new_white = self.state[0][:action_cell_index] + (action_result,) + self.state[0][action_cell_index+1:]
            self.state = (new_white, self.state[1], 'b')
        else:
            action_cell_index = self.state[1].index(action_cell)
            new_black = self.state[1][:action_cell_index] + (action_result,) + self.state[1][action_cell_index+1:]
            self.state = (self.state[0], new_black, 'w')

    def take_action(self, search_depth=8, alphabeta=True):
        children = get_children(self.state)
        if alphabeta:
            action_vals = [self.alphabeta_search(c, search_depth-1, float("-inf"), float("inf")) for c in children]
        else:
            action_vals = [self.search(c, search_depth-1) for c in children]
        print([self.action_to(s) for s in children])
        print(action_vals)
        if self.state[2] == 'w':
            best_value = max(action_vals)
        else:
            best_value = min(action_vals)
        s = children[action_vals.index(best_value)]
        action = self.action_to(s)
        self.state = s
        return action

    def action_to(self, end_state):
        if self.state[2] == 'w':
            white_start = set(self.state[0])
            white_end = set(end_state[0])
            start_cell = (white_start - white_end).pop()
            end_cell = (white_end - white_start).pop()
        else:
            black_start = set(self.state[1])
            black_end = set(end_state[1])
            start_cell = (black_start - black_end).pop()
            end_cell = (black_end - black_start).pop()
        return start_cell + inverse_mappings[(int(end_cell[0]) - int(start_cell[0]), int(end_cell[1]) - int(start_cell[1]))]

    def search(self, state, depth):
        if state[2] == 'b' and is_winning(state[0]): return 1000 + depth
        elif state[2] == 'w' and is_winning(state[1]): return -1000 - depth
        if depth == 0:
            return self.heuristic(state)
        else:
            if state[2] == 'w':
                h = float("-inf")
                for c in get_children(state):
                    h = max(h, self.search(c, depth-1))
            else:
                h = float("inf")
                for c in get_children(state):
                    h = min(h, self.search(c, depth-1))
        return h

    def alphabeta_search(self, state, depth, alpha, beta):
        if state[2] == 'b' and is_winning(state[0]): return 1000 + depth
        elif state[2] == 'w' and is_winning(state[1]): return -1000 - depth
        if depth == 0:
            return self.heuristic(state)
        else:
            if state[2] == 'w':
                h = float("-inf")
                for c in get_children(state):
                    h = max(h, self.alphabeta_search(c, depth-1, alpha, beta))
                    alpha = max(alpha, h)
                    if beta <= alpha: break
            else:
                h = float("inf")
                for c in get_children(state):
                    h = min(h, self.alphabeta_search(c, depth-1, alpha, beta))
                    beta = min(beta, h)
                    if beta <= alpha: break
        return h

    def heuristic(self, state):
        white2runs = num_rows(state[0], 2) + num_cols(state[0], 2) + num_diags(state[0], 2)
        black2runs = num_rows(state[1], 2) + num_cols(state[1], 2) + num_diags(state[1], 2)
        return white2runs - black2runs