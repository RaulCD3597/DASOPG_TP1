import socket
import sys
import time
import signal
from moneda import Moneda, Parser

class Main:
    BUFFER_SIZE = 1024
    SLEEP_TIME  = 300 # Segundo * 10; se hace eso para poder reacionar rapido a SIGINT
    run = True

    def __init__(self):
        pass

    def handler(self,sig, frame):
        print('{} received!\n'.format(sig))
        Main.run = False


    def main(self):
        signal.signal(signal.SIGINT, self.handler)
        port = 0
        try:
            port   = int(sys.argv[1])
            server = ("localhost", port)
        except:
            print("Puerto incorrecto")
            exit(1)

        self.parser = Parser()
        UDP_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        while Main.run:
            UDP_socket.sendto(bytearray(self.parser.get_json(), "utf-8"), server)
            print(UDP_socket.recvfrom(Main.BUFFER_SIZE))
            for i in range(Main.SLEEP_TIME):
                if Main.run:
                    time.sleep(0.1)
                else:
                    break

        UDP_socket.close()


app = Main()
app.main()