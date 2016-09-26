#!/usr/bin/python3

import argparse

from naive_agent import NaiveAgent
from smart_agent import SmartAgent
from game_server import GameServer

from utils.state import is_terminal
from utils.interface import display

def play(gameserv, color, big):
    computer = SmartAgent(color=color, bigboard=big)
    n = 7 if big else 5
    m = 6 if big else 4
    depth= 5 if big else 7
    while not is_terminal(computer.white, computer.black, computer.playing):
        if computer.playing == color:
            action = computer.take_action(search_depth=depth)
            gameserv.send_action(action)
            print("Player played: {}".format(action))
            display(computer.white, computer.black, n, m)
        else:
            action = gameserv.receive_action()
            print("Opponent played: {}".format(action))
            computer.receive_action(action)
            display(computer.white, computer.black, n, m)
    if computer.playing == 1:
        print("White wins!")
    else:
        print("Black wins!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch online game of dynamic connect-3, on telnet server.")
    parser.add_argument("gameID", help="ID used to coordinate with other player.")
    parser.add_argument('color', choices=('white', 'black'),
                        help="Piece color to be used by this player.")
    parser.add_argument('-b', dest="big", default=0,
                        help="Set to 1 to play on 7x6 board.")
    parser.add_argument('-s', dest="server", default="132.206.74.211",
                        help="Address of telnet server hosting game.")
    parser.add_argument('-p', dest="port", default=12345, type=int,
                        help="Port through which to connect to server.")

    args = parser.parse_args()

    player_color = 0 if args.color == 'white' else 1
    gameserv = GameServer(args.gameID, args.color, args.server, args.port)
    play(gameserv, player_color, args.big)