from itertools import combinations

from utils.runs import *

def is_repetition(actions):
    if len(actions) < 9:
        return False
    for i in range(3, round(len(actions) / 3), 3):
        if actions[-3 * i:].count(actions[-i:]) >= 3:
            return True
    return False

def is_terminal(white, black, playing):
    if playing == 0:
        return is_row(black) or is_col(black) or is_diag(black)
    else:
        return is_row(white) or is_col(white) or is_diag(white)

def gen_winning_combinations(n=5, m=4):
    cells = [(i, j) for j in range(1, m+1) for i in range(1, n+1)]
    winning_combinations = set(comb for comb in combinations(cells, 4) if is_winning(comb))
    return winning_combinations

def is_winning(cells):
    return is_row(cells) or is_col(cells) or is_diag(cells)

def get_actions(pieces, other_pieces, n=5, m=4, xstart=1, ystart=1):
    actions = []
    for i in range(4):
        for nc in __get_neighbor_cells(pieces[i], n, m, xstart, ystart):
            if nc not in pieces and nc not in other_pieces:
                actions.append((i, nc))
    return actions

def __get_neighbor_cells(cell, n=5, m=4, xstart=1, ystart=1):
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