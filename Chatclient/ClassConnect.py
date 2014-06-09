from socket import *
import time

class Con(object): 

    def __init__(self, ip, port):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((ip, port))

    def send(self, msg):
        self.s.sendall(msg.encode())

    def receive(self):

        return self.s.recv(10240)


if __name__ == '__main__':

    c = Con('localhost',8075)
    while 1:
        msg = input()
        c.send(msg)
        ans = c.receive()
        print(ans)
        time.sleep(0.01)
