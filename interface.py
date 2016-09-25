from utils import get_children

def get_move(computer):
    player = "Black" if computer.state[-1] == 'b' else "White"
    possible_moves = [computer.action_to(s) for s in get_children(computer.state)]
    while True:
        move = input("{} to play. Enter a valid move: ".format(player))
        move = move.upper()
        if move in possible_moves:
            return move
        else:
            print("That's not a valid move!!")

def display(state, n=5, m=4):
    blank = ['_,' for i in range(n * m)]
    for w in state[0]:
        index = int(w[0]) - 1 + (int(w[1]) - 1) * n
        blank[index] = '0,'
    for b in state[1]:
        index = int(b[0]) - 1 + (int(b[1]) - 1) * n
        blank[index] = '1,'
    for i in range(m):
        index = n - 1 + i * n
        blank[index] = blank[index].replace(',', '\n')
    print("".join(blank))