from utils.runs import *
from utils.state import __get_neighbor_cells

def trapped_pieces(pieces, other_pieces, n=5, m=4):
    total = 0
    for p in pieces:
        trapped = True
        for nc in __get_neighbor_cells(p, n, m):
            if nc not in pieces and nc not in other_pieces:
                trapped = False
        if trapped:
            total += 1
    return total

def mate_in_1(cells, opponent, n=5, m=4):
    row = get_row(opponent, 2)
    if row:
        if __can_complete(row, [c for c in opponent if c not in row], cells, 'r', False, n, m):
            return True
    col = get_col(opponent, 2)
    if col:
        if __can_complete(col, [c for c in opponent if c not in col], cells, 'c', False, n, m):
            return True
    diag_pp = get_diag_pp(opponent, 2)
    if diag_pp:
        if __can_complete(diag_pp, [c for c in opponent if c not in diag_pp], cells, 'p', False, n, m):
            return True
    diag_pn = get_diag_pn(opponent, 2)
    if diag_pn:
        if __can_complete(diag_pn, [c for c in opponent if c not in diag_pn], cells, 'n', False, n, m):
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

def __can_complete(run, options, avoid, run_type, block=True, n=5, m=4):
    missing_cells = __get_missing_cells(run, run_type, n, m)
    can_complete = False
    for mc in missing_cells:
        if mc in avoid: continue
        for nc in __get_neighbor_cells(mc, n, m):
            if block and nc in avoid:
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

def position_score(cells, n=5, m=4):
    score = 0
    for c in cells:
        score += cell_score(c)
    return score

def cell_score(c, n=5, m=4): # give score to cell based on distance from edge
    xscore = min(c[0] - 1, n - c[0])
    yscore = min(c[1] - 1, m - c[1])
    return (xscore * yscore) ** 4