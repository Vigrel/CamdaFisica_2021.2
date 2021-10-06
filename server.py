from enlace import *
from mirutils import bcolors
from datetime import datetime

class Server:
    def __init__(self, client_port) -> None:
        self.EOP = b'\xFF\xAA\xFF\xAA'
        self.CRC = b'\x00\x00'
        self.server_address = b'\x11'

        self.log_file = []

        self.serial_name = client_port
        self.conn = enlace(self.serial_name)
        self.conn.enable()

        self.file = bytes()

        print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + 'Conectou server')
        self.execute_server()

    def execute_server(self):
        print(bcolors.OKBLUE + "SERVER: " + bcolors.BOLD + 'Esperando mensagem' + bcolors.ENDC)
        ocioso = True
        timer = time.time()

        while ocioso:
            if self.recive_type1(): ocioso = False
            time.sleep(1)
            if time.time() - timer > 20:
                self.conn.disable()
                exit()

        self.send_type2()
        print(bcolors.OKBLUE + "SERVER: " + bcolors.BOLD + 'Na Escuta!\n\n' + bcolors.ENDC )
        self.count = 1

        while self.count <= int.from_bytes(self.num_packages, 'little'):
            timer1 = time.time()
            timer2= time.time()

            while not self.recive_type3():
                time.sleep(1)
                
                if time.time() - timer2 > 20:
                    ocioso = True 
                    self.send_type5()
                        
                if time.time() - timer1 > 2:
                    self.send_type4()
                    timer1 = time.time()
                    continue
            
            if self.pckg_ok:
                self.send_type4()
                self.count +=1
                continue
            self.send_type6(self.count.to_bytes(1,'little'))
                
        print(bcolors.OKBLUE + "\n\nSERVER:" + bcolors.BOLD + f' SUCESSO!!!' + bcolors.ENDC)
        self.conn.disable()  

        with open("img_received.png", "wb") as file:
            file.write(self.file)

        with open("log/Server3.txt", "w") as file:
            for i in self.log_file:
                file.write(i)

    def recive_type1(self):
        data, data_size = self.conn.getData(14)

        if data_size !=0:
            if data[2].to_bytes(1, "little") == self.server_address:
                now = str(datetime.now()) + ' || receb || 1 || 14' 
                self.log_file.append(now)
                print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Mensagem tipo1 recebida --> {data} ')
                self.num_packages = data[3].to_bytes(1, "little")
                return True
            print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + 'Endereço de servidor errado')
            return False
    
    def send_type2(self):
        now = '\n' + str(datetime.now()) + ' || envio || 2 || 14' 
        self.log_file.append(now)
        msgType = b'\x02' 
        type2 = msgType + b'\x01' + self.server_address + self.num_packages + b'\x00'*6 + self.EOP
        self.conn.sendData(type2)

        print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Mensagem tipo2 enviada ---> {type2}')

    def recive_type3(self):
        while True:
            head, head_size = self.conn.getData(10)

            if head_size != 0:
                payload_size = head[5]
                now = '\n' + str(datetime.now()) + f' || receb || 3 || {payload_size} || {self.count} || {self.num_packages} || {self.CRC}'
                self.log_file.append(now) 
                data, _ = self.conn.getData(payload_size + len(self.EOP))

                if head[4] != self.count or data[payload_size:] != self.EOP:
                    print(bcolors.WARNING + "SERVER: " + bcolors.BOLD + 'pacote ou tamanho errado' + bcolors.ENDC )
                    self.pckg_ok = False
                else:
                    print(bcolors.OKCYAN + "_______" + bcolors.ENDC)
                    print(bcolors.OKBLUE + "SERVER: " + bcolors.BOLD + 'pacotes de dados' + bcolors.ENDC )
                    print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Payload recebido ---> {data[0:payload_size]}')
                    self.file += data[0:payload_size]
                    self.pckg_ok = True
                return True

            return False
            
    def send_type4(self):
        now = '\n' + str(datetime.now()) + ' || envio || 4 || 14' 
        self.log_file.append(now)
        msgType = b'\x04' 
        type4 = msgType + b'\x01' + self.server_address + self.num_packages + b'\x00'*3 + self.count.to_bytes(1,'little') + b'\x00'*2 + self.EOP
        self.conn.sendData(type4)

        print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Mensagem tipo4 enviada ---> {type4}')

    def send_type5(self):
        now = '\n' + str(datetime.now()) + ' || envio || 5 || 14' 
        self.log_file.append(now)
        msgType = b'\x05' 
        type5 = msgType + b'\x00'*9 + self.EOP
        self.conn.sendData(type5)
        print(bcolors.OKBLUE + "SERVER: " + bcolors.ENDC + f'Mensagem tipo5 enviada ---> {type5}')
        print(bcolors.WARNING + "SERVER: " + f':-(' + bcolors.ENDC)
        
        with open("log/Server4.txt", "w") as file:
            for i in self.log_file:
                file.write(i)
        
        self.conn.disable() 
        exit()

    def send_type6(self, right_package):
        now = '\n' + str(datetime.now()) + ' || envio || 6 || 14' 
        self.log_file.append(now)
        msgType = b'\x06' 
        type6 = msgType + b'\x00'*5 + right_package + b'\x00'*3 + self.EOP
        self.conn.sendData(type6)
        print(bcolors.WARNING + "SERVER: " + bcolors.ENDC + f'Mensagem tipo6 enviada ---> {type6}')