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

        self.file = bytes()

        print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + 'Conectou server')
        self.execute_server()

    def execute_server(self):
        print(bcolors.OKBLUE + "SERVER: " + bcolors.BOLD + 'Esperando mensagem' + bcolors.ENDC)
        
        self.ocioso = True
        while self.ocioso:
            self.recive_type1()
        self.send_type2()
        print(bcolors.OKBLUE + "SERVER: " + bcolors.BOLD + 'Na Escuta!\n\n' + bcolors.ENDC )

        self.timer1 = time.time()
        self.timer2= time.time()
        self.count = 1

        while self.count <= int.from_bytes(self.num_packages, 'little'):
            self.recive_type3()
            self.send_type4()
            print(bcolors.OKBLUE + "SERVER: " + bcolors.BOLD + 'payload correto e num pacote esperado correto' + bcolors.ENDC )
            self.count += 1

        print(bcolors.OKBLUE + "\n\nSERVER:" + bcolors.BOLD + f' SUCESSO!!!' + bcolors.ENDC)
        self.conn.disable()  

        with open("img_received.png", "wb") as file:
            file.write(self.file)

    def recive_type1(self):
        self.data, self.data_size = self.conn.getData(14)

        if self.data_size !=0:
            if self.data[2].to_bytes(1, "little") == self.server_address:
                print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Mensagem tipo1 recebida --> {self.data} ')
                self.ocioso = False
                self.num_packages = self.data[3].to_bytes(1, "little")
                if self.data[0] != 1:
                    print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + 'Mensagem não é do tipo 1')
                    time.sleep(1)
                    self.ocioso = True

            else:
                time.sleep(1)
                print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + 'Endereço de servidor errado')
    
    def send_type2(self):
        msgType = b'\x02' 
        type2 = msgType + b'\x01' + self.server_address + self.num_packages + b'\x00'*6 + self.EOP
        self.conn.sendData(type2)

        while (self.conn.tx.getIsBussy()):
            pass

        print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Mensagem tipo2 enviada ---> {bytes(type2)}')
        self.stage1 = False

    def recive_type3(self):
        while True:
            self.head, self.head_size = self.conn.getData(10)

            if self.head_size != 0:
                payload_size = self.head[5]
                self.data, _ = self.conn.getData(payload_size + len(self.EOP))
                print(bcolors.OKCYAN + "_______" + bcolors.ENDC)
                print(bcolors.OKBLUE + "SERVER: " + bcolors.BOLD + 'pacotes de dados' + bcolors.ENDC )
                print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Payload recebido ---> {bytes(self.data[0:payload_size])}')
                self.file += self.data[0:payload_size]
                break

    def send_type4(self):
        msgType = b'\x04' 
        type4 = msgType + b'\x01' + self.server_address + self.num_packages + b'\x00'*3 + self.count.to_bytes(1,'little') + b'\x00'*2 + self.EOP
        self.conn.sendData(type4)

        while (self.conn.tx.getIsBussy()):
            pass

        print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Mensagem tipo4 enviada ---> {bytes(type4)}')









    