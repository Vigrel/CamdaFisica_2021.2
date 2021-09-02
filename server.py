from enlace import *

serialName = "COM5"      


def main():
    try:
        com1 = enlace('COM5')
        
    
        com1.enable()

        while True:

            rxBuffer, nRx = com1.getData()
            if rxBuffer != b'':
                size = (nRx-4)/2    # Número de comandos =( Recebido - 4 de referência) / 2 padronização de envio
                break

        print("recebeu uma quantia de {} dados. Equivalentes a {}" .format(int(size), rxBuffer))


        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
