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
        print(bcolors.OKBLUE + "SERVER: " + bcolors.BOLD + 'Esperando mensagem' + bcolors.ENDC)
        
        self.ocioso = True
        while self.ocioso:
            self.recive_type1()

        self.send_type2()
        self.cont = 1
        self.conn.disable()  

    def recive_type1(self):
        self.data, self.data_size = self.conn.getData(14)

        if self.data_size !=0:
            if self.data[2].to_bytes(1, "little") == self.server_address:
                print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Mensagem tipo1 recebida --> {self.data} ')
                self.ocioso = False
                if self.data[0] != 1:
                    print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + 'Mensagem não é do tipo 1')
                    time.sleep(1)
                    self.ocioso = True

            else:
                time.sleep(1)
                print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + 'Endereço de servidor errado')
    
    def send_type2(self):
        print(bcolors.OKBLUE + "SERVER: " + bcolors.BOLD + 'Na Escuta!' + bcolors.ENDC )
        msgType = b'\x02' + (0).to_bytes(9,'little')
        type2 = msgType + self.EOP
        self.conn.sendData(type2)

        while (self.conn.tx.getIsBussy()):
            pass

        print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Mensagem tipo2 enviada ---> {bytes(type2)}')
        self.stage1 = False









    