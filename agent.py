import pickle
import random
from collections import defaultdict
from utils import get_children

class Agent(object):

    def __init__(self, state="1152135451125314w", color='w', helper=0):
        self.state = state
        self.color = color
        if helper == 0:
            if color == 'w':
                self.value = 1
                with open("white_winning_states.pkl", 'rb') as f:
                    self.database = defaultdict(lambda: -1, pickle.load(f))
            else:
                self.value = -1
                with open("black_winning_states.pkl", 'rb') as f:
                    self.database = defaultdict(lambda: 1, pickle.load(f))
        elif helper == 1:
            with open("game_states.pkl", 'rb') as f:
                self.database = pickle.load(f)
        self.moves = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
        self.inverse_moves = {(0, -1): 'N', (1, 0): 'E', (0, 1): 'S', (-1, 0): 'W'}

    def receive_action(self, action):
        if self.state[-1] == 'b':
            black = [self.state[8+2*i:8+2*i+2] for i in range(4)]
            i = black.index(action[:-1])
            c = str(int(black[i][0]) + self.moves[action[-1]][0]) + str(int(black[i][1]) + self.moves[action[-1]][1])
            new_black = sorted(black[:i] + [c] + black[i+1:], key=lambda x: int(x[1] + x[0]))
            self.state = self.state[:8] + "".join(new_black) + 'w'
        else:
            white = [self.state[2*i:2*i+2] for i in range(4)]
            i = white.index(action[:-1])
            c = str(int(white[i][0]) + self.moves[action[-1]][0]) + str(int(white[i][1]) + self.moves[action[-1]][1])
            new_white = sorted(white[:i] + [c] + white[i+1:], key=lambda x: int(x[1] + x[0]))
            self.state = "".join(new_white) + self.state[8:-1] + 'b'

    def take_action(self):
        children_states = get_children(self.state)
        move_values = {}
        for s in children_states:
            if self.database[s] == 'D':
                move_values[-0.5] = s
            else:
                move_values[self.value * self.database[s]] = s
        best_value = max(move_values.keys())
        best_value = 'D' if best_value == -0.5 else self.value * best_value
        best_moves = [s for s in children_states if self.database[s] == best_value]
        s = random.choice(best_moves)
        action = self.action_to(s)
        self.state = s
        return action

    def action_to(self, end_state):
        if self.state[-1] == 'w':
            white_start = set(self.state[2*i:2*i+2] for i in range(4))
            white_end = set(end_state[2*i:2*i+2] for i in range(4))
            start_cell = (white_start - white_end).pop()
            end_cell = (white_end - white_start).pop()
        else:
            black_start = set(self.state[8+2*i:8+2*i+2] for i in range(4))
            black_end = set(end_state[8+2*i:8+2*i+2] for i in range(4))
            start_cell = (black_start - black_end).pop()
            end_cell = (black_end - black_start).pop()
        return start_cell + self.inverse_moves[(int(end_cell[0]) - int(start_cell[0]), int(end_cell[1]) - int(start_cell[1]))]