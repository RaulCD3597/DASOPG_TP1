import socket
import json
import sys
import time
import signal

class Parser:
    def __init__(self):
        pass


    @staticmethod
    def __get_config():
        try:
            with open('config.txt','r') as file:
                config = {}
                for line in file:
                    line = line.strip().split(':')
                    config[line[0].strip().lower()] = line[1].strip()
                return config
        except FileNotFoundError as error:
            print('No existe archivo de configuracion.')
            exit(error)


    @staticmethod
    def __get_monedas():
        try:
            config = Parser.__get_config()
            monedas = []
            header = True
            with open(config['path'] + config['file'],'r') as file:
                for line in file:
                    if header:
                        header = False
                    else:
                        line = line = line.strip().split(',')
                        # formato archivo: id,nombre,compra,venta
                        # formato moneda: {"id": 1, "value1": 60, "value2": 65, "name": "Dolar"}
                        moneda = {}
                        moneda['id'] = line[0]
                        moneda['value1'] = line[2]
                        moneda['value2'] = line[3]
                        moneda['name'] = line[1]
                        monedas.append(moneda)
                return monedas
        except FileNotFoundError as error:
            print('No existe archivo cambios actuales.')
            exit(error)

        
    def get_json(self):
        monedas = Parser.__get_monedas()
        return json.dumps(monedas)
            

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