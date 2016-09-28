"""These utility functions can be used to give specific information about a state.

"""

from utils.runs import *

def is_repetition(actions):
    """Check action sequence for 3-fold repetition.

    Args:
        actions (str): action sequence to check

    Returns:
        Whether 3-fold repetition exists in the actions.

    """
    if len(actions) < 9:
        return False
    for i in range(3, round(len(actions) / 3), 3):
        if actions[-3 * i:].count(actions[-i:]) >= 3:
            return True
    return False

def is_terminal(white, black, playing):
    """Check whether the state is terminal.

    Args:
        white (list): White pieces position.
        black (list): Black pieces position.
        playing (int): Identity of the player whose turn it is to make a move.

    Returns:
        Whether the state is terminal.

    """
    if playing == 0:
        return is_row(black) or is_col(black) or is_diag(black)
    else:
        return is_row(white) or is_col(white) or is_diag(white)

def is_winning(cells):
    """Check whether the cells are in a winning formation.

    Args:
        cells (list): cells to check

    Returns:
        Whether the cells are in a winning formation.

    """
    return is_row(cells) or is_col(cells) or is_diag(cells)

def get_actions(pieces, other_pieces, n=5, m=4, xstart=1, ystart=1):
    """Get possible actions given a state.

    Args:
        pieces (list): Pieces from which to move.
        other_pieces (list): Possibly blocking pieces.
        n (int): width of grid
        m (int): height of grid
        xstart (int): starting x coordinate
        ystart (int): starting y coordinate

    Returns:
        possible actions from position.

    """
    actions = []
    for i in range(4):
        for nc in _get_neighbor_cells(pieces[i], n, m, xstart, ystart):
            if nc not in pieces and nc not in other_pieces:
                actions.append((i, nc))
    return actions

def _get_neighbor_cells(cell, n=5, m=4, xstart=1, ystart=1):
    x = cell[0]
    y = cell[1]
    ncs = []
    if y != ystart:
        ncs.append((x, y-1))
    if x != xstart:
        ncs.append((x-1, y))
    if x != n:
        ncs.append((x+1, y))
    if y != m:
        ncs.append((x, y+1))
    return ncs