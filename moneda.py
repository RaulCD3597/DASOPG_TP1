import json

class Moneda(object):
    def __init__(self, id, name, value1, value2):
        self.set_id(id)
        self.set_name(name)
        self.set_value1(value1)
        self.set_value2(value2)

    # getters and setters
    def get_id(self):
        return self.__id


    def set_id(self, id):
        self.__id = id


    def get_name(self):
        return self.__name


    def set_name(self, name):
        self.__name = name


    def get_value1(self):
        return self.__value1


    def set_value1(self, value1):
        self.__value1 = value1


    def get_value2(self):
        return self.__value2


    def set_value2(self, value2):
        self.__value2 = value2

    # public funtions
    def to_dictionary(self):
        dic = {}
        dic['id']     = self.get_id()
        dic['name']   = self.get_name()
        dic['value1'] = self.get_value1()
        dic['value2'] = self.get_value2()
        return dic


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
                        moneda = Moneda(line[0], line[1], line[2], line[3])
                        monedas.append(moneda.to_dictionary())
                return monedas
        except FileNotFoundError as error:
            print('No existe archivo cambios actuales.')
            exit(error)

        
    def get_json(self):
        monedas = Parser.__get_monedas()
        return json.dumps(monedas)