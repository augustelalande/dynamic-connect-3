def is_terminal(state):
    if state[2] == 'w':
        return is_winning(state[1])
    else:
        return is_winning(state[0])

def is_repetition(actions):
    if len(actions) < 9:
        return False
    for i in range(3, round(len(actions) / 3), 3):
        if actions[-3 * i:].count(actions[-i:]) >= 3:
            return True
    return False

def is_winning(cells):
    return num_rows(cells) or num_cols(cells) or num_diags(cells)

def get_children(state):
    children = []
    if state[2] == 'w': # white to move
        for i in range(4):
            for nc in neighbor_cells(state[0][i]):
                if nc not in state[0] and nc not in state[1]:
                    new_white = state[0][:i] + (nc,) + state[0][i+1:]
                    children.append((new_white, state[1], 'b'))
    else:
        for i in range(4):
            for nc in neighbor_cells(state[1][i]):
                if nc not in state[0] and nc not in state[1]:
                    new_black = state[1][:i] + (nc,) + state[1][i+1:]
                    children.append((state[0], new_black, 'w'))
    return children

def neighbor_cells(cell, n=5, m=4):
    x = int(cell[0])
    y = int(cell[1])
    ncs = []
    if y != 1:
        ncs.append(str(x) + str(y-1))
    if x != 1:
        ncs.append(str(x-1) + str(y))
    if x != n:
        ncs.append(str(x+1) + str(y))
    if y != m:
        ncs.append(str(x) + str(y+1))
    return ncs

def num_rows(cells, length=3):
    num = 0
    cells = sorted(cells, key=lambda x: int(x[1]) * 10 + int(x[0]))
    sequence_count = 1
    for i in range(len(cells)-1):
        if cells[i][1] == cells[i+1][1] and int(cells[i][0]) + 1 == int(cells[i+1][0]):
            sequence_count += 1
        else:
            sequence_count = 1
        if sequence_count == length:
            num += 1
            sequence_count -= 1
    return num

def num_cols(cells, length=3):
    num = 0
    cells = sorted(cells, key=lambda x: int(x))
    sequence_count = 1
    for i in range(len(cells)-1):
        if cells[i][0] == cells[i+1][0] and int(cells[i][1]) + 1 == int(cells[i+1][1]):
            sequence_count += 1
        else:
            sequence_count = 1
        if sequence_count == length:
            num += 1
            sequence_count -= 1
    return num

def num_diags(cells, length=3):
    num = 0
    diag1 = sorted(cells, key=lambda x: int(x[0]) - int(x[1]) + int(x[1]) / 10)
    diag2 = sorted(cells, key=lambda x: int(x[0]) + int(x[1]) + int(x[1]) / 10)
    sequence_count1 = 1
    sequence_count2 = 1
    for i in range(len(cells)-1):
        if int(diag1[i][0]) + 1 == int(diag1[i+1][0]) and int(diag1[i][1]) + 1 == int(diag1[i+1][1]):
            sequence_count1 += 1
        else:
            sequence_count1 = 1
        if int(diag2[i][0]) - 1 == int(diag2[i+1][0]) and int(diag2[i][1]) + 1 == int(diag2[i+1][1]):
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