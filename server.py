from enlace import *
from mirutils import bcolors

class Server:
    def __init__(self, client_port) -> None:
        self.EOP = b'\xFF\xAA\xFF\xAA'
        self.CRC = b'\x00\x00'
        self.server_address = b'\x11'

        self.serial_name = client_port
        self.conn = enlace(self.serial_name)
        self.conn.enable()
        print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + 'Conectou server')

        self.execute_server()

    def execute_server(self):
        print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + 'Esperando mensagem')
        self.running = True

        while self.running:
            self.recive_type1()
            self.send_type2()

        self.conn.disable()  

    def recive_type1(self):
        self.data, self.data_size = self.conn.getData(14)

        if self.data_size !=0:
            if self.data[2].to_bytes(1, "little") == self.server_address:
                print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Mensagem tipo1 recebida --> {self.data} ')
                assert self.data[0] == 1, bcolors.WARNING + "ERROR: " + bcolors.ENDC + 'Mensagem não é do tipo 1'
            else:
                print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + 'Endereço de servidor errado')










    