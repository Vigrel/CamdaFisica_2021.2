from typing import List
from enlace import *

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

def send(conn: enlace, head: List[bytes], payload: List[bytes], eop: List[bytes]):
    data = head + payload + eop
    conn.sendData(data)
    print(f"\nSending data: {data}\n")

def receive(conn: enlace, size: int):
    data, data_size = conn.getData(size)
    print(f"\nReceiving data: {data}\n")

    return data, data_size

def parse_data(data: bytes):

    header = data[:10]
    payload = data[10:-4]
    eop = data[-4:]

    print()
    print(bcolors.UNDERLINE + "Parsing received data" + bcolors.ENDC)
    print("-"*21)
    print(f"Header:{header}\n")
    print(f"Payload:{payload}\n")
    print(f"EOP:{eop}")
    print(bcolors.UNDERLINE + "-"*21 + bcolors.ENDC)
    print()

    return header, payload, eop 