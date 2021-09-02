#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################

from enlace import *
import time
import numpy as np
import random

serialName = "COM6"      


def main():
    try:
        com1 = enlace('COM6')
        
    
        com1.enable()
        """ 
        SERVER
        """

        command = b'\x00' + b'_'
        command2 = b'\x0F'+ b'_'
        command3 = b'\x00' + b'\xFF'+ b'_'
        command4 = b'\xFF' + b'\x00'+ b'_'
        command5 = b'\xFF'+ b'_'
        command6 = b'\xF0'+ b'_'

        dataList = [command, command2, command3, command4, command5, command6 ]

        randNumber = random.randint(10,30)

  
        print(f"numero aleatorio igual a {randNumber}")
        
        dados_enviados = []
        # dado_inicial = np.asarray(b'\x22')
        com1.sendData(b'\x22')

        # dados_enviados.append(dado_inicial)
        print(f'dado inicial enviado')

        for i in range(randNumber):
            txBuffer = random.choice(dataList)
            # dado = np.asarray(txBuffer)
            com1.sendData(txBuffer)
            print(txBuffer)
            # dados_enviados.append(dado)


        # dado_final = np.asarray(b'\x11')
        com1.sendData(b'\x11')
        # dados_enviados.append(dado_final)

        # print(f"Meus dados: {dados_enviados}")
       
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
