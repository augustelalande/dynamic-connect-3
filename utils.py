def is_terminal(computer):
    if computer.playing == 0:
        return is_winning(computer.black)
    else:
        return is_winning(computer.white)

def is_repetition(actions):
    if len(actions) < 9:
        return False
    for i in range(3, round(len(actions) / 3), 3):
        if actions[-3 * i:].count(actions[-i:]) >= 3:
            return True
    return False

def is_winning(cells):
    return num_rows(cells) or num_cols(cells) or num_diags(cells)

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

def num_rows(cells, length=3):
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

def num_cols(cells, length=3):
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

def num_diags(cells, length=3):
    num = 0
    diag1 = sorted(cells, key=lambda x: x[0] - x[1] + x[1] / 10)
    diag2 = sorted(cells, key=lambda x: x[0] + x[1] + x[1] / 10)
    sequence_count1 = 1
    sequence_count2 = 1
    for i in range(len(cells)-1):
        if diag1[i][0] + 1 == diag1[i+1][0] and diag1[i][1] + 1 == diag1[i+1][1]:
            sequence_count1 += 1
        else:
            sequence_count1 = 1
        if diag2[i][0] - 1 == diag2[i+1][0] and diag2[i][1] + 1 == diag2[i+1][1]:
            sequence_count2 += 1
        else:
            sequence_count2 = 1
        if sequence_count1 == length:
            num += 1
            sequence_count1 -= 1
        if sequence_count2 == length:
            num += 1
            sequence_count2 -= 1
    return num

inverse_mappings = {(0, -1): 'N', (1, 0): 'E', (0, 1): 'S', (-1, 0): 'W'}

def action_string(start_cell, end_cell):
    return "{}{}".format(*start_cell) + inverse_mappings[(end_cell[0] - start_cell[0], end_cell[1] - start_cell[1])]