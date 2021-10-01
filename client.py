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
        print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + 'Conectou client')

        self.execute_client()

    def execute_client(self):
        self.running = True

        for i in range(5):
            self.send_type1()
            time.sleep(2) 

        self.conn.disable()  
        
    def send_type1(self):
        msgType = b'\x01'
        numPackages = b'\x01'
        actualPackege = b'\x00'
        head = msgType + b'\x01' + self.server_address + numPackages + actualPackege + b'\x00\x00\x00' + self.CRC
        type1 = head + self.EOP

        self.conn.rx.clearBuffer()
        self.conn.sendData(type1)

        while (self.conn.tx.getIsBussy()):
            pass

        print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo1 enviada ---> {bytes(type1)}')
        print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + 'Quero Falar com você')
