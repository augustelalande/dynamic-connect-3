from utils.interface import action_string
from utils.state import get_actions, is_winning
from utils.runs import num_runs

action_mappings = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}

class NaiveAgent(object):
    """Dynamic connect-3 game playing agent.

        Args:
            color (int): Piece color to be used by this agent. 0 for white, 1 for black.
            bigboard (int, optional): 0 to indicate the use og 5x4 grid, 1 for 7x6 grid.

    """

    def __init__(self, color, bigboard=0):
        if bigboard:
            self.n = 7
            self.m = 6
            self.white = [(2, 2), (2, 4), (6, 3), (6, 5)]
            self.black = [(2, 3), (2, 5), (6, 2), (6, 4)]
        else:
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

    def take_action(self, search_depth=7, alphabeta=True):
        """Searches through the game tree and chooses the move it thinks is optimal.

        Args:
            search_depth (int): Max depth to look through the game tree.
            alphabeta (bool): Indicate whether to use alphabeta prunning or not.

        Returns:
            str: Action string of found move.

        """
        actions = get_actions(self.pieces, self.opponent, self.n, self.m)
        if alphabeta:
            action_vals = [self._alphabeta_search(a, search_depth - 1, float("-inf"), float("inf")) for a in actions]
        else:
            action_vals = [self._search(a, search_depth-1) for a in actions]
        if self.color == 0:
            best_value = max(action_vals)
        else:
            best_value = min(action_vals)
        best_action = actions[action_vals.index(best_value)]
        action = action_string(self.pieces[best_action[0]], best_action[1])
        self.pieces[best_action[0]] = best_action[1]
        self.playing = 1 if self.color == 0 else 0
        return action

    def _search(self, action, depth):
        """Implementation of depth-limited search.

        This search works by updating the game state with the possible actions at each node and recursively
        descending through the game tree until either a terminal node is reached or the depth goes to zero
        at which point it returns the heuristic value of the game state.

        When comming back up the game tree it undoes the changes it made so that different branches can be explored.

        """
        if self.playing == 0: # apply the action that was passed
            self.playing = 1
            tmp_cell = self.white[action[0]]
            self.white[action[0]] = action[1]
        else:
            self.playing = 0
            tmp_cell = self.black[action[0]]
            self.black[action[0]] = action[1]

        if self.playing == 1 and is_winning(self.white): # check for terminal states
            val = 100000 + depth
        elif self.playing == 0 and is_winning(self.black):
            val = -100000 - depth
        elif depth == 0: # if depth reaches zero return the estimate value of the game state
            val = self._heuristic()
        else:
            if self.playing == 0: # otherwise iterate through each child node and return the best value determined using minimax
                val = float("-inf")
                for a in get_actions(self.white, self.black, self.n, self.m):
                    val = max(val, self._search(a, depth-1))
            else:
                val = float("inf")
                for a in get_actions(self.black, self.white, self.n, self.m):
                    val = min(val, self._search(a, depth-1))

        if self.playing == 0: # undo the action that was made at the beggining of the call
            self.playing = 1
            self.black[action[0]] = tmp_cell
        else:
            self.playing = 0
            self.white[action[0]] = tmp_cell
        return val

    def _alphabeta_search(self, action, depth, alpha, beta):
        """Implementation of depth-limited search using alphabeta prunning.

        This search works identically to the one above (_search) but implements alphabeta prunning
        to get rid of unworthwhile branches.

        """
        if self.playing == 0: # apply the action that was passed
            self.playing = 1
            tmp_cell = self.white[action[0]]
            self.white[action[0]] = action[1]
        else:
            self.playing = 0
            tmp_cell = self.black[action[0]]
            self.black[action[0]] = action[1]

        if self.playing == 1 and is_winning(self.white): # check for terminal states
            val = 1000 + depth
        elif self.playing == 0 and is_winning(self.black):
            val = -1000 - depth
        elif depth == 0: # if depth reaches zero return the estimate value of the game state
            val= self._heuristic()
        else:
            if self.playing == 0: # otherwise iterate through each child node and return the best value determined using minimax and alphabeta prunning
                val = float("-inf")
                for a in get_actions(self.white, self.black, self.n, self.m):
                    val = max(val, self._alphabeta_search(a, depth-1, alpha, beta))
                    alpha = max(alpha, val) # update alpha if better value found
                    if beta <= alpha: break # if alpha >= beta then this branch will not be selected so stop searching
            else:
                val = float("inf")
                for a in get_actions(self.black, self.white, self.n, self.m):
                    val = min(val, self._alphabeta_search(a, depth-1, alpha, beta))
                    beta = min(beta, val) # update beta if better value found
                    if beta <= alpha: break # if beta <= alpha then this branch will not be selected so stop searching

        if self.playing == 0: # undo the action that was made at the beggining of the call
            self.playing = 1
            self.black[action[0]] = tmp_cell
        else:
            self.playing = 0
            self.white[action[0]] = tmp_cell
        return val

    def _heuristic(self):
        """Simple heuristic to evaluate a game state.

        Returns:
            int: <number of runs of 2 white pieces> - <number of runs of 2 black pieces>

        """
        white2runs = num_runs(self.white, 2)
        black2runs = num_runs(self.black, 2)
        return white2runs - black2runs