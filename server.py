from mirutils import send, receive, parse_data
from enlace import *

serialName = "COM8"      

HANDSHAKE = 1
MESSAGE = 0
GREETINGS = 0

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


def handshake(conn: enlace):
    global HANDSHAKE, MESSAGE

    print()
    print(bcolors.HEADER + "HANDSHAKE" + bcolors.ENDC)
    print("="*9)
    print(bcolors.HEADER + "Receiving handshake data from client and sending a response" + bcolors.ENDC)
    print()

    data, data_size = receive(conn, 128)

    _, file_size, _ = parse_data(data)

    file_size = int.from_bytes(file_size, byteorder="little")

    print(f"Message size to receive (in bytes): {file_size}")

    head = b'\x11' * 10 
    payload = b''
    eop = b'\x11' * 4

    send(conn, head, payload, eop)

    HANDSHAKE, MESSAGE = 0, 1

    return file_size 


def receive_message(conn: enlace, file_size: int):
    global MESSAGE, GREETINGS, HANDSHAKE

    print()
    print(bcolors.OKCYAN + "RECEIVING MESSAGE" + bcolors.ENDC)
    print("="*14)
    print(bcolors.OKCYAN + "Receiving message in packages from client and responding with confirmations" + bcolors.ENDC)
    print()

    last_index = 0
    last_package_size = file_size % 114

    print(bcolors.OKGREEN + f"Receiving Package {last_index + 1}" + bcolors.ENDC)

    data, data_size = receive(conn, 128)
    
    head, payload, eop = parse_data(data)

    index, fragments_size = int.from_bytes(head[:5], byteorder='little'), int.from_bytes(head[5:], byteorder='little')

    while (index != last_index + 1) or (len(eop) != 4):
        print(bcolors.WARNING + f"Package {last_index + 1} is corrupted. Asking for re-sending." + bcolors.ENDC)
        
        send(conn, b'\x11' * 10 , b'', b'\x00' * 4)

        print(bcolors.OKGREEN + f"Receiving Package {last_index + 1}" + bcolors.ENDC)

        data, data_size = receive(conn, 128)
        
        head, payload, eop = parse_data(data)

        index, fragments_size = int.from_bytes(head[:5], byteorder='little'), int.from_bytes(head[5:], byteorder='little')

    print(bcolors.BOLD + f"Package {last_index + 1} received succesfully" + bcolors.ENDC)
    print()

    picture = payload
    last_index = index
    
    print("Sending confirmation to client")
    send(conn, b'\x11' * 10 , b'', b'\x11' * 4)

    for fragment_index in range(1, fragments_size):

        print(bcolors.OKGREEN + f"Receiving Package {last_index + 1}" + bcolors.ENDC)
            
        if fragment_index != fragments_size - 1:
            data, data_size = receive(conn, 128)
        else:
            data, data_size = receive(conn, last_package_size + 14)
            
            if data_size == 0:
                print(bcolors.FAIL + "Message size was incorrect. Asking for re-sending all transmission again" + bcolors.ENDC)
                send(conn, b'\x00' * 10 , b'', b'\x00' * 4)

                MESSAGE, HANDSHAKE = 0, 1
                
                return None 
        
        head, payload, eop = parse_data(data)

        index, _ = int.from_bytes(head[:5], byteorder='little'), int.from_bytes(head[5:], byteorder='little')

        while (index != last_index + 1) or (len(eop) != 4):
            print(bcolors.WARNING + f"Package {last_index + 1} is corrupted. Asking for re-sending." + bcolors.ENDC)
            
            send(conn, b'\x11' * 10 , b'', b'\x00' * 4)

            print(bcolors.OKGREEN + f"Receiving Package {last_index + 1}" + bcolors.ENDC)

            data, data_size = receive(conn, 128)
            
            head, payload, eop = parse_data(data)

            index, fragments_size = int.from_bytes(head[:5], byteorder='little'), int.from_bytes(head[5:], byteorder='little')

        print(bcolors.BOLD + f"Package {last_index + 1} received succesfully" + bcolors.ENDC)
        print()

        picture += payload
        last_index = index

        print("Sending confirmation to client")
        send(conn, b'\x11' * 10 , b'', b'\x11' * 4)

    with open("img_received.png", "wb") as file:
        file.write(picture)
    
    MESSAGE, GREETINGS = 0, 1

def greetings(conn: enlace):
    print()
    print(bcolors.OKBLUE + "GREETINGS" + bcolors.ENDC)
    print("="*9)
    print(bcolors.OKBLUE + "Sending message to end transmission" + bcolors.ENDC)
    print()

    send(conn, b'\x11' * 10 , b'', b'\x11' * 4)

    return "Succesfull transmission!" 

def main():
    conn = enlace(serialName)
    conn.enable()

    while True:
        try:
            if HANDSHAKE:
                file_size = handshake(conn)
            elif MESSAGE:
                receive_message(conn, file_size)
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