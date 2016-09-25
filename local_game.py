import argparse

from naive_agent import NaiveAgent
from utils import is_terminal, is_repetition
from interface import *

def play(w='h', b='h'):
    actions = ""
    if w == 'h' and b == 'h': # human vs human
        computer = NaiveAgent()
        display(computer)
        while not is_terminal(computer) and not is_repetition(actions):
            action = get_move(computer)
            actions += action
            computer.receive_action(action)
            display(computer)
    elif w == 'c' and b == 'c': # computer vs computer
        # computer = NaiveAgent()
        # display(computer)
        # while not is_terminal(computer) and not is_repetition(actions):
        #     action = computer.take_action(search_depth=7)
        #     actions += action
        #     print("Computer played: {}".format(action))
        #     display(computer)
        pass
    else:
        computer_color = 0 if w == 'c' else 1
        computer = NaiveAgent(color=computer_color)
        display(computer)
        while not is_terminal(computer) and not is_repetition(actions):
            if computer.playing == computer_color:
                action = computer.take_action()
                actions += action
                print("Computer played: {}".format(action))
                display(computer)
            else:
                action = get_move(computer)
                actions += action
                computer.receive_action(action)
                display(computer)
    if is_repetition(actions):
        print("Draw!")
    elif computer.playing == 1:
        print("White wins!")
    else:
        print("Black wins!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch local game of dynamic connect-3.")
    parser.add_argument("white", choices=('h', 'c'),
                        help="White player. Either 'h' for human or 'c' for computer.")
    parser.add_argument("black", choices=('h', 'c'),
                        help="Black player. Either 'h' for human or 'c' for computer.")

    args = parser.parse_args()
    play(w=args.white, b=args.black)