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

        dataList = [0, 15, 255, 65280,255, 240]
        dataList = ['0000', '0F00', '00FF', 'FF00', 'FF00', 'F000']

        randNumber = random.randint(10,30)

  
        print(f"numero aleatorio igual a {randNumber}")
        
        dados_enviados = []

        print(f'dado inicial enviado')

        for i in range(randNumber):
            txBuffer = random.choice(dataList)
            print(txBuffer)
            dados_enviados.append(txBuffer)


        dados_enviados.insert(0, "E000")
        dados_enviados.append("1100")
        dados_enviados = " ".join(dados_enviados)
        
        
        dados_bytes = bytearray.fromhex(dados_enviados)

        com1.sendData(dados_bytes)
        print(f"Meus dados: {dados_bytes}")
       
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
