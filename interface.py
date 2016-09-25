from agent import Agent
from utils import *

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

def display(state):
    blank = ['_,' for i in range(23)]
    for i in range(23):
        if i % 6 == 5:
            blank[i] = '\n'
    white = [state[2*i:2*i+2] for i in range(4)]
    black = [state[8+2*i:8+2*i+2] for i in range(4)]
    for w in white:
        index = int(w[0]) - 1 + (int(w[1]) - 1) * 6
        blank[index] = '0,'
    for b in black:
        index = int(b[0]) - 1 + (int(b[1]) - 1) * 6
        blank[index] = '1,'
    print("".join(blank))

def play(w='h', b='h', computer_assistance=True):
    actions = ""
    if w == 'h' and b == 'h': # human vs human
        if computer_assistance:
            computer = Agent(helper=1)
        else:
            computer = Agent(helper=2)
        display(computer.state)
        while not is_terminal(computer.state) and not is_repetition(actions):
            if computer_assistance:
                for s in get_children(computer.state):
                    print(computer.action_to(s), computer.database[s])
            action = get_move(computer)
            actions += action
            computer.receive_action(action)
            display(computer.state)
        if computer.state[-1] == 'b':
            print("White wins!")
        else:
            print("Black wins!")
    elif w == 'c' and b == 'c': # computer vs computer
        white = Agent(color='w')
        black = Agent(color='b')
        while not is_terminal(white.state) and not is_repetition(actions):
            if white.state[-1] == 'w': # white to play
                action = white.take_action()
                actions += action
                black.receive_action(action)
                print("White played: {}".format(action))
                display(white.state)
            else:
                action = black.take_action()
                actions += action
                white.receive_action(action)
                print("Black played: {}".format(action))
                display(white.state)
        if white.state[-1] == 'b':
            print("White wins!")
        else:
            print("Black wins!")
    else:
        computer_color = 'w' if w == 'c' else 'b'
        computer = Agent(color=computer_color)
        display(computer.state)
        while not is_terminal(computer.state) and not is_repetition(actions):
            if computer.state[-1] == computer_color:
                for s in get_children(computer.state):
                        print(computer.action_to(s), computer.database[s])
                action = computer.take_action()
                actions += action
                print("Computer played: {}".format(action))
                display(computer.state)
            else:
                if computer_assistance:
                    for s in get_children(computer.state):
                        print(computer.action_to(s), computer.database[s])
                action = get_move(computer)
                actions += action
                computer.receive_action(action)
                display(computer.state)
        if computer.state[-1] == computer_color:
            print("\nCONGRATULATIONS YOU BEAT THE ARTIFICIAL \"\"\"INTELIGENCE\"\"\"")
        else:
            print("\nI GUESS HUMANITY IS DOOMED AFTER ALL")

if __name__ == "__main__":
    play(w='c', b='c', computer_assistance=False)