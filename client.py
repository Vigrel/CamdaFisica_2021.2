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
        with open('file.png', "rb") as file:
            read_data = file.read()

        fragments = [read_data[i:i+114] for i in range(0, len(read_data), 114)]
        fragments_size = len(fragments)

        while not self.inicia:
            self.send_type1(fragments_size)
            print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + 'Quero Falar com você' + bcolors.ENDC )
            time.sleep(5)
            self.recive_type2()
            print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + 'Na Escuta\n\n' + bcolors.ENDC )
        
        self.count = 1

        while self.count <= fragments_size:
            self.send_type3(fragments, fragments_size)
            print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + f'pckg')
            # self.timer1 = time.time()
            # print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + f'reenvio' + bcolors.ENDC)
            # self.timer2= time.time()
            # print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + f'time out' + bcolors.ENDC)

            self.recive_type4()
        
        print(bcolors.HEADER + "\n\nCLIENT:" + bcolors.BOLD + f' SUCESSO!!!' + bcolors.ENDC)

        self.conn.disable()  
        
    def send_type1(self, fragments_size):
        msg_type = b'\x01'
        num_packages = fragments_size.to_bytes(1,'little') 
        package_id = b'\x00'
        head = msg_type + b'\x01' + self.server_address + num_packages + package_id + b'\x00\x00\x00' + self.CRC
        type1 = head + self.EOP

        self.conn.rx.clearBuffer()
        self.conn.sendData(type1)

        while (self.conn.tx.getIsBussy()):
            pass

        print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo1 enviada ---> {bytes(type1)}')

    def recive_type2(self):
        self.data, self.data_size = self.conn.getData(14)

        if self.data_size !=0:
            if self.data[0] == 2:
                print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo2 recebida --> {self.data} ')
                self.inicia = True
            else:
                print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + 'Mensagem não é do tipo 2')

    def send_type3(self, fragments, fragments_size):
    
        msg_type = b'\x03'
        sensor_id = b'\x01'
        num_packages = fragments_size.to_bytes(1,'little') 
        error_package = b'\x00'
        package_id = (self.count).to_bytes(1,'little')
        payload = fragments[self.count - 1]
        payload_size = (len(payload)).to_bytes(1,'little')
        last_package = (self.count - 1).to_bytes(1,'little')

        if self.count == 1:
            last_package = (self.count).to_bytes(1,'little')
            
        head = msg_type + sensor_id + self.server_address + num_packages + package_id + payload_size + error_package + last_package + self.CRC
        type3 = head + payload + self.EOP
        print(bcolors.OKCYAN + "_______" + bcolors.ENDC)
        print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo3 enviada --> {type3}')
        self.conn.sendData(type3)

    def recive_type4(self):
        self.data, self.data_size = self.conn.getData(14)
        if self.data_size !=0:
            if self.data[0] == 4:
                print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo4 recebida --> {self.data} ')
                self.count += 1
            else:
                print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + 'Mensagem não é do tipo 4')
            