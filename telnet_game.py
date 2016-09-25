#!/usr/bin/python3

import argparse

from naive_agent import NaiveAgent
from game_server import GameServer

from interface import display
from utils import is_terminal

def play(gameserv, color):
    computer = NaiveAgent(color=color)
    while not is_terminal(computer.state):
        if computer.state[2] == color:
            action = computer.take_action()
            gameserv.send_action(action)
            print("Player played: {}".format(action))
            display(computer.state)
        else:
            action = gameserv.receive_action()
            print("Opponent played: {}".format(action))
            computer.receive_action(action)
            display(computer.state)
    if computer.state[2] == 'b':
        print("White wins!")
    else:
        print("Black wins!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch online game of dynamic connect-3, on telnet server.")
    parser.add_argument("gameID", help="ID used to coordinate with other player.")
    parser.add_argument('color', choices=('w', 'b', 'white', 'black'),
                        help="Piece color to be used by this player.")
    parser.add_argument('-s', dest="server", default="132.206.74.211",
                        help="Address of telnet server hosting game.")
    parser.add_argument('-p', dest="port", default=12345, type=int,
                        help="Port through which to connect to server.")

    args = parser.parse_args()

    color = 'w' if args.color == 'w' or args.color == 'white' else 'b'
    gameserv = GameServer(args.gameID, color, args.server, args.port)
    play(gameserv, color)