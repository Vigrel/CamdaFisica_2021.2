from mirutils import send, receive
from enlace import *
import time

serialName = "COM7"      
img_path = 'img.png'

with open(img_path, "rb") as file:
    read_data = file.read()

HANDSHAKE = 1
MESSAGE = 0
GREETINGS = 0

start = time.time()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def handshake(conn: enlace, incorrect_size: bool):
    global HANDSHAKE, MESSAGE

    print()
    print(bcolors.HEADER + "HANDSHAKE" + bcolors.ENDC)
    print("="*9)
    print(bcolors.HEADER + "Sending handshake data to server and receiving its response" + bcolors.ENDC)
    print()

    head = b'\x11' * 10 
    payload = (len(read_data) + 1).to_bytes(114, "little")
    eop = b'\x11' * 4

    if incorrect_size:
        payload = (len(read_data)).to_bytes(114, "little")
        time.sleep(2)

    send(conn, head, payload, eop)

    data, data_size = receive(conn, 14)

    while data_size == 0:
        user_response = input(bcolors.FAIL + "Servidor inativo. Tentar novamente? S/N\n" + bcolors.ENDC)
        if user_response != "S":
            print("Cancelling connection")
            return False
        
        send(conn, head, payload, eop)

        data, data_size = receive(conn, 14)

    HANDSHAKE, MESSAGE = 0, 1

    return True

def send_message(conn: enlace):
    global MESSAGE, GREETINGS, HANDSHAKE

    print()
    print(bcolors.OKCYAN + "SENDING MESSAGE" + bcolors.ENDC)
    print("="*14)
    print(bcolors.OKCYAN + "Sending message to server in packages and checking for confirmations" + bcolors.ENDC)
    print()
    
    fragments = [read_data[i:i+114] for i in range(0, len(read_data), 114)]
    fragments_size = len(fragments)

    for index, fragment in enumerate(fragments):
            
        head = (index + 1).to_bytes(5, byteorder='little') + (fragments_size).to_bytes(5, byteorder='little')
        payload = fragment
        eop = b'\x11' * 4

        # Creating a corrupted package to test failures
        if index == 1:
            head = (index + 2).to_bytes(5, byteorder='little') + (fragments_size).to_bytes(5, byteorder='little')

        print(bcolors.OKGREEN + f"Sending Package {index + 1}" + bcolors.ENDC)
        send(conn, head, payload, eop)

        print("Waiting for confirmation from server")
        data, data_size = receive(conn, 14)

        while data != b"\x11" * 14:

            if data == b"\x00" * 14:
                print(bcolors.FAIL + f"Message size was corrupted. Starting transmission again..." + bcolors.ENDC)
                MESSAGE, HANDSHAKE = 0, 1
                return True

            print(bcolors.FAIL + f"Package {index + 1} was corrupted. Sending it again..." + bcolors.ENDC)
            print()

            # Sending normal package to test if server responds to failures
            if index == 1:
                head = (index + 1).to_bytes(5, byteorder='little') + (fragments_size).to_bytes(5, byteorder='little')
            
            print(bcolors.OKGREEN + f"Sending Package {index + 1}" + bcolors.ENDC)
            send(conn, head, payload, eop)

            print("Waiting for confirmation from server")
            data, data_size = receive(conn, 14)
        
        print(bcolors.BOLD + f"Package {index + 1} sended succesfully" + bcolors.ENDC)
        print()

    MESSAGE, GREETINGS = 0, 1

def greetings(conn: enlace):
    print()
    print(bcolors.OKBLUE + "GREETINGS" + bcolors.ENDC)
    print("="*9)
    print(bcolors.OKBLUE + "Receiving message to end transmission" + bcolors.ENDC)
    print()

    data, data_size = receive(conn, 14)

    if data != b"\x11" * 14: return "Transmission failed"

    return "Succesfull transmission!" 

def main():
    conn = enlace(serialName)
    conn.enable()

    incorrect_size = False

    while True:
        try:
            if HANDSHAKE:
                if not handshake(conn, incorrect_size):
                    break
            elif MESSAGE:
                incorrect_size = send_message(conn)
            elif GREETINGS:
                print(greetings(conn))
                break
        except Exception as erro:
            print("ops! :-\\")
            print(erro)
            conn.disable()
        
    conn.disable()
    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()