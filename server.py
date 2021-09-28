from enlace import *

class Server:
    def __init__(self, client_port) -> None:
        self.EOP = b'0xFF0xAA0xFF0xAA'
        self.CRC = b'0x000x00'
        self.server_address = b'0x11'

        self.serial_name = client_port
        self.conn = enlace(self.serial_name)
        self.conn.enable()
        print('Conectou server')

        self.execute_server()

    def execute_server(self):
        print('Esperando mensagem')
        self.running = True

        while self.running:
            self.recive_type1()

        self.send_type2()        

    def recive_type1(self):
        self.data, self.data_size = self.conn.getData(14)
        
        if self.data[2] == self.server_address:
            self.numberOfPackets = int.from_bytes(self.request[2:5], 'little')
            self.currentPacket = 0
            self.expectedPacket = 1
            self.idle = False

        
    def send_type2(self):

        pass
        
    def recive_type3():
        pass
        
    def recive_type4():
        pass
            
    def recive_type5():
        pass
        
    def recive_type6():
        pass












    