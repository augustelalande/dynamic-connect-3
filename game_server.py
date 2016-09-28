from telnetlib import Telnet
# from time import

class GameServer(object):
    """This class provides an abstraction to the telnet server hosting the games.

        Args:
            gameID (str): ID with which the game will be hosted.
            color (str): Color of the local player. white or black.
            server (str): Address used to connect to the host server.
            port (int): port through which to connect to the server
    """

    def __init__(self, gameID, color, server, port):
        print("Connecting to {}:{}...".format(server, port))
        self.tn = Telnet(server, port) # establish connection to the server
        msg = "{} {}\n".format(gameID, color).encode('ASCII')
        print("Starting game '{}' as {}...".format(gameID, color))
        self.tn.write(msg) # send initial message indicating gameID and local player color
        return_msg = self.tn.read_until(b'\n')
        if return_msg == msg: # verify game was started correctly
            print("Game successfully started.")
            if color == "white":
                print("Preparing first move.")
            else:
                print("Waiting for opponent's move.")
        else:
            print(return_msg.decode()) # if print the error message sent by the server
            raise Exception("Unable to start game.") # and crash the program

    def send_action(self, action):
        """Send local players action to the server.

        Args:
            action (str): Action string to be sent.

        """
        msg = "{}\n".format(action).encode('ASCII')
        self.tn.write(msg) # send action to server
        return_msg = self.tn.read_until(b'\n') # wait for response
        if return_msg != msg: # if unexpected response
            print(return_msg.decode())
            raise Exception("Unable to send action.") # crash the program

    def receive_action(self):
        """Recieve opponents action from the server.

        Returns:
            str: Action sent by opponent.

        """
        msg = self.tn.read_until(b'\n') # wait for the server to send a move
        action = msg.decode()[:-1]
        if len(action) != 3: # if move does not seem valid
            print(action)
            raise Exception("Invalid action received.") # crash the program
        return action