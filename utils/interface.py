from utils.state import get_actions

def get_move(white, black, playing, n=5, m=4):
    player_color = "White" if playing == 0 else "Black"
    player = white if playing == 0 else black
    opponent = white if playing == 1 else black
    possible_moves = [action_string(player[a[0]], a[1]) for a in get_actions(player, opponent, n, m)]
    while True:
        move = input("{} to play. Enter a valid move: ".format(player_color))
        move = move.upper()
        if move in possible_moves:
            return move
        else:
            print("That's not a valid move!!")

def display(white, black, n=5, m=4):
    blank = ['_,' for i in range(n * m)]
    for w in white:
        index = w[0] - 1 + (w[1] - 1) * n
        blank[index] = '0,'
    for b in black:
        index = b[0] - 1 + (b[1] - 1) * n
        blank[index] = '1,'
    for i in range(m):
        index = n - 1 + i * n
        blank[index] = blank[index].replace(',', '\n')
    print("".join(blank))

inverse_mappings = {(0, -1): 'N', (1, 0): 'E', (0, 1): 'S', (-1, 0): 'W'}

def action_string(start_cell, end_cell):
    return "{}{}".format(*start_cell) + inverse_mappings[(end_cell[0] - start_cell[0], end_cell[1] - start_cell[1])]