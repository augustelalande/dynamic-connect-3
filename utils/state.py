from utils.runs import *

def is_terminal(white, black, playing):
    if playing == 0:
        return is_row(black) or is_col(black) or is_diag(black)
    else:
        return is_row(white) or is_col(white) or is_diag(white)

def is_repetition(actions):
    if len(actions) < 9:
        return False
    for i in range(3, round(len(actions) / 3), 3):
        if actions[-3 * i:].count(actions[-i:]) >= 3:
            return True
    return False

def is_winning(cells, opponent):
    return is_row(cells) or is_col(cells) or is_diag(cells) or mate_in_2(cells, opponent)

def mate_in_2(cells, opponent):
    return False

def get_actions(pieces, other_pieces):
    actions = []
    for i in range(4):
        for nc in neighbor_cells(pieces[i]):
            if nc not in pieces and nc not in other_pieces:
                actions.append((i, nc))
    return actions

def neighbor_cells(cell, n=5, m=4):
    x = cell[0]
    y = cell[1]
    ncs = []
    if y != 1:
        ncs.append((x, y-1))
    if x != 1:
        ncs.append((x-1, y))
    if x != n:
        ncs.append((x+1, y))
    if y != m:
        ncs.append((x, y+1))
    return ncs