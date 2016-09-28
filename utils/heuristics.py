"""These utility functions can be used to estimate the value of a particular position.

"""

from math import sqrt
from utils.runs import *
from utils.state import _get_neighbor_cells

def piece_seperation(pieces):
    xsum = 0
    ysum = 0
    for p in pieces:
        xsum += p[0]
        ysum += p[1]
    center = (round(xsum / 4), round(ysum / 4))
    seperation = 0
    for p in pieces:
        seperation += _distance(center, p)
    return seperation

def trapped_pieces(pieces, other_pieces, n=5, m=4):
    """Calculate the number of pieces that are unable to move.

    Args:
        pieces (list): Pieces from which to count.
        other_pieces (list): Possibly blocking pieces.
        n (int): width of grid
        m (int): height of grid

    Returns:
        Number of blocked pieces.

    """
    total = 0
    for p in pieces:
        trapped = True
        for nc in _get_neighbor_cells(p, n, m):
            if nc not in pieces and nc not in other_pieces:
                trapped = False
        if trapped:
            total += 1
    return total

def scored_runs(cells, n=5, m=4):
    """Attribute a score to each run based on how easy it is to complete.

    Args:
        cells (list): Pieces top check for runs.
        n (int): width of grid
        m (int): height of grid

    Returns:
        Total score.

    """
    score = 0

    row = get_row(cells, 2)
    if row:
        missing_cells = _get_missing_cells(row, 'r', n, m)
        min_distance = float("inf")
        if len(missing_cells) != 0:
            for c in cells:
                if c not in row:
                    min_distance = min(min_distance, *[_distance(c, mc) for mc in missing_cells])
        score += min_distance
    col = get_col(cells, 2)
    if col:
        missing_cells = _get_missing_cells(col, 'c', n, m)
        min_distance = float("inf")
        if len(missing_cells) != 0:
            for c in cells:
                if c not in col:
                    min_distance = min(min_distance, *[_distance(c, mc) for mc in missing_cells])
        score += min_distance
    diag_pp = get_diag_pp(cells, 2)
    if diag_pp:
        missing_cells = _get_missing_cells(diag_pp, 'p', n, m)
        min_distance = float("inf")
        if len(missing_cells) != 0:
            for c in cells:
                if c not in diag_pp:
                    min_distance = min(min_distance, *[_distance(c, mc) for mc in missing_cells])
        score += min_distance
    diag_pn = get_diag_pn(cells, 2)
    if diag_pn:
        missing_cells = _get_missing_cells(diag_pn, 'n', n, m)
        min_distance = float("inf")
        if len(missing_cells) != 0:
            for c in cells:
                if c not in diag_pn:
                    min_distance = min(min_distance, *[_distance(c, mc) for mc in missing_cells])
        score += min_distance
    return -score

def _distance(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

def pattern_check(cells):
    """Check the cells for a specific pattern which I found to be good.

    Args:
        pieces (list): Pieces from which to check.

    Returns:
        Whether the pattern exists.

    """
    cells = sorted(cells, key=lambda x: x[1] * 10 + x[0])
    if cells[0][1] + 1 == cells[1][1] and cells[0][0] + 1 == cells[1][0]:
        if cells[1][1] + 1 == cells[2][1] and cells[1][0] == cells[2][0]:
            if cells[2][1] + 1 == cells[3][1] and cells[2][0] + 1 == cells[3][0]:
                return True
    elif cells[0][1] + 1 == cells[1][1] and cells[0][0] - 1 == cells[1][0]:
        if cells[1][1] + 1 == cells[2][1] and cells[1][0] == cells[2][0]:
            if cells[2][1] + 1 == cells[3][1] and cells[2][0] - 1 == cells[3][0]:
                return True
    return False


def mate_in_1(cells, opponent, n=5, m=4):
    """Check the cells for a mate in 1.

    Args:
        cells (list): Cells pieces which may mate the opponent in 2 moves.
        opponent (list): Opponent pieces which may br in the way.
        n (int): width of grid
        m (int): height of grid

    Returns:
        Whether mate in 1 will occur.

    """
    row = get_row(cells, 2)
    if row:
        if _can_complete(row, [c for c in cells if c not in row], opponent, 'r', False, n, m):
            return True
    col = get_col(cells, 2)
    if col:
        if _can_complete(col, [c for c in cells if c not in col], opponent, 'c', False, n, m):
            return True
    diag_pp = get_diag_pp(cells, 2)
    if diag_pp:
        if _can_complete(diag_pp, [c for c in cells if c not in diag_pp], opponent, 'p', False, n, m):
            return True
    diag_pn = get_diag_pn(cells, 2)
    if diag_pn:
        if _can_complete(diag_pn, [c for c in cells if c not in diag_pn], opponent, 'n', False, n, m):
            return True
    return False

def mate_in_2(cells, opponent, n=5, m=4):
    """Check the cells for a mate in 2

    Args:
        cells (list): Cells pieces which may mate the opponent in 2 moves.
        opponent (list): Opponent pieces which may get in the way.
        n (int): width of grid
        m (int): height of grid

    Returns:
        Whether mate in 2 will occur.

    """

    row = get_row(cells, 2)
    if row:
        if _can_complete(row, [c for c in cells if c not in row], opponent, 'r', n, m):
            return True
    col = get_col(cells, 2)
    if col:
        if _can_complete(col, [c for c in cells if c not in col], opponent, 'c', n, m):
            return True
    diag_pp = get_diag_pp(cells, 2)
    if diag_pp:
        if _can_complete(diag_pp, [c for c in cells if c not in diag_pp], opponent, 'p', n, m):
            return True
    diag_pn = get_diag_pn(cells, 2)
    if diag_pn:
        if _can_complete(diag_pn, [c for c in cells if c not in diag_pn], opponent, 'n', n, m):
            return True
    return False

def _can_complete(run, options, avoid, run_type, block=True, n=5, m=4):
    missing_cells = _get_missing_cells(run, run_type, n, m)
    can_complete = False
    for mc in missing_cells:
        if mc in avoid: continue
        for nc in _get_neighbor_cells(mc, n, m):
            if block and nc in avoid:
                return False
            if not can_complete and nc in options:
                can_complete = True
    return can_complete

def _get_missing_cells(run, run_type, n=5, m=4):
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
    """Give a score to the placement of the cells. central cells are worth more

    Args:
        cells (list): Cells to check.
        n (int): width of grid
        m (int): height of grid

    Returns:
        Position score.

    """
    score = 0
    for c in cells:
        score += _cell_score(c)
    return score

def _cell_score(c, n=5, m=4): # give score to cell based on distance from edge
    xscore = min(c[0] - 1, n - c[0])
    yscore = min(c[1] - 1, m - c[1])
    return (xscore * yscore) ** 4