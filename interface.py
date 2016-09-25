from utils import get_actions, action_string

def get_move(computer):
    player = "Black" if computer.color == 0 else "White"
    possible_moves = [action_string(computer.opponent[a[0]], a[1]) for a in get_actions(computer.opponent, computer.pieces)]
    while True:
        move = input("{} to play. Enter a valid move: ".format(player))
        move = move.upper()
        if move in possible_moves:
            return move
        else:
            print("That's not a valid move!!")

def display(computer, n=5, m=4):
    blank = ['_,' for i in range(n * m)]
    for w in computer.white:
        index = w[0] - 1 + (w[1] - 1) * n
        blank[index] = '0,'
    for b in computer.black:
        index = b[0] - 1 + (b[1] - 1) * n
        blank[index] = '1,'
    for i in range(m):
        index = n - 1 + i * n
        blank[index] = blank[index].replace(',', '\n')
    print("".join(blank))