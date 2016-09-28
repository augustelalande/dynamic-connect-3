"""These utility functions are used to know everything about runs.

"""

def is_row(cells):
    """Check if run of 3 exists in cell rows.

    Args:
        cells (list): Cells to check.

    Returns:
        Whether the cells form a 3 run row.

    """
    cells = sorted(cells, key=lambda x: x[1] * 10 + x[0])
    sequence_count = 1
    for i in range(len(cells)-1):
        if cells[i][1] == cells[i+1][1] and cells[i][0] + 1 == cells[i+1][0]:
            sequence_count += 1
        else:
            sequence_count = 1
        if sequence_count == 3: # winning row
            return True
    return False

def is_col(cells):
    """Check if run of 3 exists in cell columns.

    Args:
        cells (list): Cells to check.

    Returns:
        Whether the cells form a 3 run column.

    """
    cells = sorted(cells, key=lambda x: x[0] * 10 + x[1])
    sequence_count = 1
    for i in range(len(cells)-1):
        if cells[i][0] == cells[i+1][0] and cells[i][1] + 1 == cells[i+1][1]:
            sequence_count += 1
        else:
            sequence_count = 1
        if sequence_count == 3:
            return True
    return False

def is_diag(cells):
    """Check if run of 3 exists in cell diags.

    Args:
        cells (list): Cells to check.

    Returns:
        Whether the cells form a 3 run diagonal.

    """
    diag_pp = sorted(cells, key=lambda x: x[0] - x[1] + x[1] / 10)
    diag_pn = sorted(cells, key=lambda x: x[0] + x[1] + x[1] / 10)
    sequence_count_pp = 1
    sequence_count_pn = 1
    for i in range(len(cells)-1):
        if diag_pp[i][0] + 1 == diag_pp[i+1][0] and diag_pp[i][1] + 1 == diag_pp[i+1][1]:
            sequence_count_pp += 1
        else:
            sequence_count_pp = 1
        if diag_pn[i][0] - 1 == diag_pn[i+1][0] and diag_pn[i][1] + 1 == diag_pn[i+1][1]:
            sequence_count_pn += 1
        else:
            sequence_count_pn = 1
        if sequence_count_pp == 3 or sequence_count_pn == 3:
            return True
    return False

def num_runs(cells, length):
    """Calculate number of runs of certain length.

    Args:
        cells (list): Cells to check.
        length (int): length of run to count.

    Returns:
        Number of runs of length length.

    """
    return num_rows(cells, length) + num_cols(cells, length) + num_diags(cells, length)

def num_rows(cells, length):
    """Calculate number of row runs of certain length.

    Args:
        cells (list): Cells to check.
        length (int): length of run to count.

    Returns:
        Number of row runs of length length.

    """
    num = 0
    cells = sorted(cells, key=lambda x: x[1] * 10 + x[0])
    sequence_count = 1
    for i in range(len(cells)-1):
        if cells[i][1] == cells[i+1][1] and cells[i][0] + 1 == cells[i+1][0]:
            sequence_count += 1
        else:
            sequence_count = 1
        if sequence_count == length:
            num += 1
            sequence_count -= 1
    return num

def num_cols(cells, length):
    """Calculate number of column runs of certain length.

    Args:
        cells (list): Cells to check.
        length (int): length of run to count.

    Returns:
        Number of column runs of length length.

    """
    num = 0
    cells = sorted(cells, key=lambda x: x[0] * 10 + x[1])
    sequence_count = 1
    for i in range(len(cells)-1):
        if cells[i][0] == cells[i+1][0] and cells[i][1] + 1 == cells[i+1][1]:
            sequence_count += 1
        else:
            sequence_count = 1
        if sequence_count == length:
            num += 1
            sequence_count -= 1
    return num

def num_diags(cells, length):
    """Calculate number of diagonal runs of certain length.

    Args:
        cells (list): Cells to check.
        length (int): length of run to count.

    Returns:
        Number of diagonal runs of length length.

    """
    num = 0
    diag_pp = sorted(cells, key=lambda x: x[0] - x[1] + x[1] / 10)
    diag_pn = sorted(cells, key=lambda x: x[0] + x[1] + x[1] / 10)
    sequence_count_pp = 1
    sequence_count_pn = 1
    for i in range(len(cells)-1):
        if diag_pp[i][0] + 1 == diag_pp[i+1][0] and diag_pp[i][1] + 1 == diag_pp[i+1][1]:
            sequence_count_pp += 1
        else:
            sequence_count_pp = 1
        if diag_pn[i][0] - 1 == diag_pn[i+1][0] and diag_pn[i][1] + 1 == diag_pn[i+1][1]:
            sequence_count_pn += 1
        else:
            sequence_count_pn = 1
        if sequence_count_pp == length:
            num += 1
            sequence_count_pp -= 1
        if sequence_count_pn == length:
            num += 1
            sequence_count_pn -= 1
    return num

def get_row(cells, length):
    """Get cells which form a row run of a certain length.

    Args:
        cells (list): Cells to check.
        length (int): length of run to count.

    Returns:
        Cells forming row run.

    """
    cells = sorted(cells, key=lambda x: x[1] * 10 + x[0])
    row = [cells[0]]
    for i in range(len(cells)-1):
        if cells[i][1] == cells[i+1][1] and cells[i][0] + 1 == cells[i+1][0]:
            row.append(cells[i+1])
        else:
            row = [cells[i+1]]
        if len(row) == length:
            return row
    return []

def get_col(cells, length):
    """Get cells which form a column run of a certain length.

    Args:
        cells (list): Cells to check.
        length (int): length of run to count.

    Returns:
        Cells forming column run.

    """
    cells = sorted(cells, key=lambda x: x[0] * 10 + x[1])
    col = [cells[0]]
    for i in range(len(cells)-1):
        if cells[i][0] == cells[i+1][0] and cells[i][1] + 1 == cells[i+1][1]:
            col.append(cells[i+1])
        else:
            col = [cells[i+1]]
        if len(col) == length:
            return col
    return []

def get_diag_pp(cells, length):
    """Get cells which form a diagonal run in +x +y direction of a certain length.

    Args:
        cells (list): Cells to check.
        length (int): length of run to count.

    Returns:
        Cells forming diagonal run  in +x +y direction.

    """
    cells = sorted(cells, key=lambda x: x[0] - x[1] + x[1] / 10)
    diag_pp = [cells[0]]
    for i in range(len(cells)-1):
        if cells[i][0] + 1 == cells[i+1][0] and cells[i][1] + 1 == cells[i+1][1]:
            diag_pp.append(cells[i+1])
        else:
            diag_pp = [cells[i+1]]
        if len(diag_pp) == length:
            return diag_pp
    return []

def get_diag_pn(cells, length):
    """Get cells which form a diagonal run in +x -y direction of a certain length.

    Args:
        cells (list): Cells to check.
        length (int): length of run to count.

    Returns:
        Cells forming diagonal run  in +x -y direction.

    """
    cells = sorted(cells, key=lambda x: x[0] + x[1] + x[1] / 10)
    diag_pn = [cells[0]]
    for i in range(len(cells)-1):
        if cells[i][0] - 1 == cells[i+1][0] and cells[i][1] + 1 == cells[i+1][1]:
            diag_pn.append(cells[i+1])
        else:
            diag_pn = [cells[i+1]]
        if len(diag_pn) == length:
            return diag_pn
    return []