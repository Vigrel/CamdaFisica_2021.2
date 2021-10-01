from enlace import *
from mirutils import bcolors

class Client:
    def __init__(self, client_port) -> None:
        self.EOP = b'\xFF\xAA\xFF\xAA'
        self.CRC = b'\x00\x00'
        self.server_address = b'\x11'

        self.serial_name = client_port
        self.conn = enlace(self.serial_name)
        self.conn.enable()
        print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + 'Conectou client' + bcolors.ENDC)

        self.execute_client()

    def execute_client(self):
        self.inicia = False

        while not self.inicia:
            self.send_type1()
            time.sleep(5)
            self.recive_type2()
        
        self.count = 1
        self.conn.disable()  
        
    def send_type1(self):
        msg_type = b'\x01'
        num_packages = b'\x01'
        actual_packege = b'\x00'
        head = msg_type + b'\x01' + self.server_address + num_packages + actual_packege + b'\x00\x00\x00' + self.CRC
        type1 = head + self.EOP

        self.conn.rx.clearBuffer()
        self.conn.sendData(type1)

        while (self.conn.tx.getIsBussy()):
            pass

        print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo1 enviada ---> {bytes(type1)}')
        print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + 'Quero Falar com você' + bcolors.ENDC )


    def recive_type2(self):
        self.data, self.data_size = self.conn.getData(14)

        if self.data_size !=0:
            if self.data[0] == 2:
                print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo2 recebida --> {self.data} ')
                print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + 'Na Escuta' + bcolors.ENDC )
                self.inicia = True
            else:
                print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + 'Mensagem não é do tipo 2')