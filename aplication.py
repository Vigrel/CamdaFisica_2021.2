import argparse
from Client import Client
from Server import Server

if __name__ == "__main__":
    # Serial Com Port
    # para saber a sua porta, execute no terminal:
    # python -m serial.tools.list_ports
    client = Client("COM5")
    server = Server("COM6")