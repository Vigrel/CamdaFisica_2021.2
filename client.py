import binascii
from enlace import *
from mirutils import bcolors
from datetime import datetime

class Client:
    def __init__(self, client_port) -> None:
        self.EOP = b'\xFF\xAA\xFF\xAA'
        self.server_address = b'\x11'

        self.log_file = []
        self.test_phase = True

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

        timer = time.time()
        while not self.inicia:
            self.send_type1(fragments_size) 
            if time.time() - timer> 20:
                self.conn.disable()
                exit()
            print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + 'Quero Falar com você' + bcolors.ENDC )
            time.sleep(5)
            self.recive_type2()
            print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + 'Na Escuta\n\n' + bcolors.ENDC )

        self.count = 1

        while self.count <= fragments_size:
            self.send_type3(fragments, fragments_size)
            timer1 = time.time()
            print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + f'reenvio' + bcolors.ENDC)
            timer2= time.time()
            print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + f'time out' + bcolors.ENDC)

            while not self.recive_type4():
                if time.time() - timer1 > 5:
                    self.send_type3(fragments, fragments_size)
                    timer1 = time.time()
                
                if time.time() - timer2 > 20:
                    print(bcolors.WARNING + "\n\nCLIENT:" + bcolors.BOLD + f'time out' + bcolors.ENDC)
                    self.send_type5()

                try:
                    if self.data_type4[0] == 6:
                        self.recive_type6(self.data_type4)
                except:
                    pass

            self.count += 1

        print(bcolors.HEADER + "\n\nCLIENT:" + bcolors.BOLD + f' SUCESSO!!!' + bcolors.ENDC)

        with open("log/Client2.txt", "w") as file:
            for i in self.log_file:
                file.write(i)

        self.conn.disable()
        
    def send_type1(self, fragments_size):
        now = str(datetime.now()) + ' || envio || 1 || 14' 
        self.log_file.append(now)
        msg_type = b'\x01'
        num_packages = fragments_size.to_bytes(1,'little') 
        package_id = b'\x00'
        head = msg_type + b'\x01' + self.server_address + num_packages + package_id + b'\x00\x00\x00' + b'\x00\x00'
        type1 = head + self.EOP

        self.conn.rx.clearBuffer()
        self.conn.sendData(type1)
        
        print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo1 enviada ---> {type1}')

    def recive_type2(self):
        data, data_size = self.conn.getData(14)

        if data_size !=0:
            now = '\n' + str(datetime.now()) + ' || receb || 2 || 14'
            self.log_file.append(now)
            if data[0] == 2:
                    print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo2 recebida --> {data} ')
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
        crc = (binascii.crc_hqx(payload, 0)).to_bytes(2, 'little')
        head = msg_type + sensor_id + self.server_address + num_packages + package_id + payload_size + error_package + last_package + crc

        now = '\n' + str(datetime.now()) + f' || envio || 3 || {len(payload)} || {self.count} || {num_packages} || {crc}'
        self.log_file.append(now)

        if self.test_phase and self.count == 2:
            self.test_phase = False
            head = msg_type + sensor_id + self.server_address + num_packages + (4).to_bytes(1,'little') + payload_size + error_package + last_package + crc
                
        type3 = head + payload + self.EOP

        print(bcolors.OKCYAN + "_______" + bcolors.ENDC)
        print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo3 enviada --> {type3}')
        self.conn.sendData(type3)
        print(bcolors.HEADER + "CLIENT: " + bcolors.BOLD + f'pckg')

    def recive_type4(self):
        data, data_size = self.conn.getData(14)
        self.data_type4 = data
        if data_size !=0:
            now = '\n' + str(datetime.now()) + ' || receb || 4 || 14'
            self.log_file.append(now)
            if data[0] == 4:
                print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo4 recebida --> {data} ')
                return True
        return False
    
    def send_type5(self):
        now = '\n' + str(datetime.now()) + ' || envio || 5 || 14'
        self.log_file.append(now)
        msgType = b'\x05' 
        type5 = msgType + b'\x00'*9 + self.EOP
        self.conn.sendData(type5)

        print(bcolors.HEADER + "CLIENT: " + bcolors.ENDC + f'Mensagem tipo5 enviada ---> {type5}')
        print(bcolors.WARNING + "CLIENT: " + f'timed out' + bcolors.ENDC)
        print(bcolors.WARNING + "CLIENT: " + f':-(' + bcolors.ENDC)
        self.conn.disable() 
        exit()
    
    def recive_type6(self, head):
        now = '\n' + str(datetime.now()) + ' || receb || 6 || 14'
        self.log_file.append(now)
        print(bcolors.HEADER + "CLIENT:" + bcolors.BOLD + f'pacote errado' + bcolors.ENDC)
        print(bcolors.WARNING + "CLIENT: " + f'Mensagem tipo6 recebia ---> {head}' + bcolors.ENDC)
        self.count = head[6]