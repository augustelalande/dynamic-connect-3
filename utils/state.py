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

def mate(cells):
    return is_row(cells) or is_col(cells) or is_diag(cells)

def mate_in_1(cells, opponent, n=5, m=4):
    row = get_row(opponent, 2)
    if row:
        if __can_complete(row, [c for c in opponent if c not in row], cells, 'r', n, m):
            return True
    col = get_col(opponent, 2)
    if col:
        if __can_complete(col, [c for c in opponent if c not in col], cells, 'c', n, m):
            return True
    diag_pp = get_diag_pp(opponent, 2)
    if diag_pp:
        if __can_complete(diag_pp, [c for c in opponent if c not in diag_pp], cells, 'p', n, m):
            return True
    diag_pn = get_diag_pn(opponent, 2)
    if diag_pn:
        if __can_complete(diag_pn, [c for c in opponent if c not in diag_pn], cells, 'n', n, m):
            return True
    return False

def mate_in_2(cells, opponent, n=5, m=4):
    row = get_row(cells, 2)
    if row:
        if __can_complete(row, [c for c in cells if c not in row], opponent, 'r', n, m):
            return True
    col = get_col(cells, 2)
    if col:
        if __can_complete(col, [c for c in cells if c not in col], opponent, 'c', n, m):
            return True
    diag_pp = get_diag_pp(cells, 2)
    if diag_pp:
        if __can_complete(diag_pp, [c for c in cells if c not in diag_pp], opponent, 'p', n, m):
            return True
    diag_pn = get_diag_pn(cells, 2)
    if diag_pn:
        if __can_complete(diag_pn, [c for c in cells if c not in diag_pn], opponent, 'n', n, m):
            return True
    return False

def __can_complete(run, options, avoid, run_type, n=5, m=4):
    missing_cells = __get_missing_cells(run, run_type, n, m)
    can_complete = False
    for mc in missing_cells:
        if mc in avoid: continue
        for nc in __get_neighbor_cells(mc, n, m):
            if nc in avoid:
                return False
            if not can_complete and nc in options:
                can_complete = True
    return can_complete

def __get_missing_cells(run, run_type, n=5, m=4):
    missing_cells = []
    if run_type == 'r':
        missing_cells.append((run[0][0] - 1, run[0][1]))
        missing_cells.append((run[1][0] + 1, run[1][1]))
    elif run_type == 'c':
        missing_cells.append((run[0][0], run[0][1] - 1))
        missing_cells.append((run[1][0], run[1][1] + 1))
    elif run_type == 'p':
        if run[0][0] != 1 and run[0][1] != 1:
            missing_cells.append((run[0][0] - 1, run[0][1] - 1))
        if run[1][0] != n and run[1][1] != m:
            missing_cells.append((run[1][0] + 1, run[1][1] + 1))
    else:
        if run[0][0] != n and run[0][1] != 1:
            missing_cells.append((run[0][0] + 1, run[0][1] - 1))
        if run[1][0] != 1 and run[1][1] != m:
            missing_cells.append((run[1][0] - 1, run[1][1] + 1))
    return missing_cells


def get_actions(pieces, other_pieces, n=5, m=4):
    actions = []
    for i in range(4):
        for nc in __get_neighbor_cells(pieces[i], n, m):
            if nc not in pieces and nc not in other_pieces:
                actions.append((i, nc))
    return actions

def __get_neighbor_cells(cell, n=5, m=4):
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