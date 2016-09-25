from telnetlib import Telnet

class GameServer(object):

    def __init__(self, gameID, color, server, port):
        print("Connecting to {}:{}...".format(server, port))
        self.tn = Telnet(server, port)
        c = "white" if color == 'w' else "black"
        msg = "{} {}\n".format(gameID, c).encode('ASCII')
        print("Starting game '{}' as {}...".format(gameID, c))
        self.tn.write(msg)
        return_msg = self.tn.read_until(b'\n')
        if return_msg == msg:
            print("Game successfully started.")
            if color == 'w':
                print("Preparing first move.")
            else:
                print("Waiting for opponents move.")
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
        action = self.tn.read_until(b'\n')
        return action.decode()[:-1]