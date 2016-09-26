import argparse

from time import clock

from naive_agent import NaiveAgent
from smart_agent import SmartAgent

from utils.state import is_terminal, is_repetition
from utils.interface import display, get_move

def play(w='h', b='h'):
    actions = ""
    if w == 'h' and b == 'h': # human vs human
        computer = NaiveAgent()
        display(computer.white, computer.black)
        while not is_terminal(computer.white, computer.black, computer.playing) and not is_repetition(actions):
            action = get_move(computer.white, computer.black, computer.playing)
            actions += action
            computer.receive_action(action)
            display(computer.white, computer.black)
    elif w == 'c' and b == 'c': # computer vs computer
        c1 = NaiveAgent(color=1)
        c2 = SmartAgent(color=0)
        display(c1.white, c1.black)
        t = clock()
        while not is_terminal(c1.white, c1.black, c1.playing) and not is_repetition(actions):
            if c1.playing == c1.color:
                action = c1.take_action(search_depth=7)
                print(clock() - t)
                t = clock()
                c2.receive_action(action)
                actions += action
                print("C1 ({}) played: {}".format(c1.color, action))
                display(c1.white, c1.black)
            else:
                action = c2.take_action(search_depth=7)
                print(clock() - t)
                t = clock()
                c1.receive_action(action)
                actions += action
                print("C2 ({}) played: {}".format(c2.color, action))
                display(c2.white, c2.black)
        computer = c1
    else:
        computer_color = 0 if w == 'c' else 1
        computer = NaiveAgent(color=computer_color)
        display(computer.white, computer.black)
        while not is_terminal(computer.white, computer.black, computer.playing) and not is_repetition(actions):
            if computer.playing == computer_color:
                action = computer.take_action()
                actions += action
                print("Computer played: {}".format(action))
                display(computer.white, computer.black)
            else:
                action = get_move(computer.white, computer.black, computer.playing)
                actions += action
                computer.receive_action(action)
                display(computer.white, computer.black)
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