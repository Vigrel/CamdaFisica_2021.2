import argparse
from client import Client
from server import Server

if __name__ == "__main__":
    # Serial Com Port
    # para saber a sua porta, execute no terminal:
    # python -m serial.tools.list_ports
    server = Server("COM8")