def is_terminal(state):
    if state[-1] == 'w':
        black = [state[8+2*i:8+2*i+2] for i in range(4)]
        return is_winning(black)
    else:
        white = [state[2*i:2*i+2] for i in range(4)]
        return is_winning(white)

def is_repetition(actions):
    if len(actions) < 9:
        return False
    for i in range(3, round(len(actions) / 3), 3):
        if actions[-3 * i:].count(actions[-i:]) >= 3:
            return True
    return False

def is_winning(cells):
    return is_row(cells) or is_col(cells) or is_diag(cells)

def is_row(cells):
    count = 0
    for i in range(len(cells)-1):
        if cells[i][1] == cells[i+1][1] and int(cells[i][0]) + 1 == int(cells[i+1][0]):
            count += 1
        else:
            count = 0
        if count == 2:
            return True
    return False

def is_col(cells):
    cells = sorted(cells, key=lambda x: int(x))
    count = 0
    for i in range(len(cells)-1):
        if cells[i][0] == cells[i+1][0] and int(cells[i][1]) + 1 == int(cells[i+1][1]):
            count += 1
        else:
            count = 0
        if count == 2:
            return True
    return False

def is_diag(cells):
    diag1 = sorted(cells, key=lambda x: int(x[0]) - int(x[1]))
    diag2 = sorted(cells, key=lambda x: int(x[0]) + int(x[1]))
    count1 = 0
    count2 = 0
    for i in range(len(cells)-1):
        if int(diag1[i][0]) + 1 == int(diag1[i+1][0]) and int(diag1[i][1]) + 1 == int(diag1[i+1][1]):
            count1 += 1
        else:
            count1 = 0
        if int(diag2[i][0]) - 1 == int(diag2[i+1][0]) and int(diag2[i][1]) + 1 == int(diag2[i+1][1]):
            count2 += 1
        else:
            count2 = 0
        if count1 == 2 or count2 == 2:
            return True
    return False

def get_parents(state):
    if state[-1] == 'b': # white just moved
        p_states = []
        white = [state[2*i:2*i+2] for i in range(4)]
        filled_cells = [state[2*i:2*i+2] for i in range(8)]
        for i in range(4):
            for nc in neighbor_cells(white[i]):
                if nc not in filled_cells:
                    new_white = sorted(white[:i] + [nc] + white[i+1:], key=lambda x: int(x[1] + x[0]))
                    p_states.append("".join(new_white) + state[8:-1] + 'w')
    else:
        p_states = []
        black = [state[8+2*i:8+2*i+2] for i in range(4)]
        filled_cells = [state[2*i:2*i+2] for i in range(8)]
        for i in range(4):
            for nc in neighbor_cells(black[i]):
                if nc not in filled_cells:
                    new_black = sorted(black[:i] + [nc] + black[i+1:], key=lambda x: int(x[1] + x[0]))
                    p_states.append(state[:8] + "".join(new_black) + 'b')
    return p_states

def get_children(state):
    if state[-1] == 'w': # white to move
        p_states = []
        white = [state[2*i:2*i+2] for i in range(4)]
        black = [state[8+2*i:8+2*i+2] for i in range(4)]
        if is_winning(black):
            return ["BLACK_WON"]
        filled_cells = [state[2*i:2*i+2] for i in range(8)]
        for i in range(4):
            for nc in neighbor_cells(white[i]):
                if nc not in filled_cells:
                    new_white = sorted(white[:i] + [nc] + white[i+1:], key=lambda x: int(x[1] + x[0]))
                    p_states.append("".join(new_white) + state[8:-1] + 'b')
    else:
        p_states = []
        black = [state[8+2*i:8+2*i+2] for i in range(4)]
        white = [state[2*i:2*i+2] for i in range(4)]
        if is_winning(white):
            return ["WHITE_WON"]
        filled_cells = [state[2*i:2*i+2] for i in range(8)]
        for i in range(4):
            for nc in neighbor_cells(black[i]):
                if nc not in filled_cells:
                    new_black = sorted(black[:i] + [nc] + black[i+1:], key=lambda x: int(x[1] + x[0]))
                    p_states.append(state[:8] + "".join(new_black) + 'w')
    return p_states

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