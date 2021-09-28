from enlace import *

class Client:
    def __init__(self, client_port) -> None:
        self.EOP = b'0xFF0xAA0xFF0xAA'
        self.CRC = b'0x000x00'
        self.server_address = b'0x11'

        self.serial_name = client_port
        self.conn = enlace(self.serial_name)
        self.conn.enable()
        print('Conectou client')
        self.execute_client()

    def execute_client(self):
        self.running = True

        while self.running:
            self.send_type1()
            self.recive_type2()
        
        self.sendData()

    def send_type1(self):
        msgType = b'0x01'
        numPackages = b'0x01'
        actualPackege = b'0x00'
        head = msgType + b'0x01' + self.server_address + numPackages + actualPackege + b'0x000x000x00' + self.CRC
        
        type1 = head + self.EOP
        self.conn.sendData(type1)

        print('Quero Falar com você')
        
    def recive_type2(self):
        self.build_head(self, b'0x02', b'0xFF' )
        pass
        
    def send_type3(self, msg):
        self.build_head(self, b'0x02', b'0xFF' )
        pass
        
    def send_type4():
        pass
        
    def send_type5():
        pass
        
    def send_type6():
        pass    
        
    def recive_type2():
        
        pass    