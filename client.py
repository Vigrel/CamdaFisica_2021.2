#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################

from enlace import *
import random

serialName = "COM6"      


def main():
    try:
        com1 = enlace('COM6')
        com1.enable()

        dataDict = {'00FF': 255, '0000': 0, '000F': 15, '00F0':240, 'FF00': 65280, '00FF': 255}
        dados_enviados = []

        randNumber = random.randint(10,30)
        print(f"numero aleatorio igual a {randNumber}\n")

        print("Dados enviados:")
        for i in range(randNumber):
            txBuffer = random.choice(list(dataDict.keys()))
            dados_enviados.append(txBuffer)

            byte = txBuffer
            num = dataDict[byte]
            print(f'{byte} --> ({num})')

        dados_enviados = " ".join(dados_enviados)
        dados_bytes = bytearray.fromhex(dados_enviados)

        com1.sendData(dados_bytes)
        print(f"\nMeus dados: {dados_bytes}")
       
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
