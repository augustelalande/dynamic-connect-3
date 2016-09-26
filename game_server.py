from telnetlib import Telnet

class GameServer(object):

    def __init__(self, gameID, color, server, port):
        print("Connecting to {}:{}...".format(server, port))
        self.tn = Telnet(server, port)
        msg = "{} {}\n".format(gameID, color).encode('ASCII')
        print("Starting game '{}' as {}...".format(gameID, color))
        self.tn.write(msg)
        return_msg = self.tn.read_until(b'\n')
        if return_msg == msg:
            print("Game successfully started.")
            if color == "white":
                print("Preparing first move.")
            else:
                print("Waiting for opponent's move.")
        else:
            print(return_msg.decode())
            raise Exception("Unable to start game.")

    def send_action(self, action):
        msg = "{}\n".format(action).encode('ASCII')
        self.tn.write(msg)
        return_msg = self.tn.read_until(b'\n')
        if return_msg != msg:
            print(return_msg.decode())
            raise Exception("Unable to send action.")

    def receive_action(self):
        msg = self.tn.read_until(b'\n')
        action = msg.decode()[:-1]
        if len(action) != 3:
            print(action)
            raise Exception("Invalid action received.")
        return action