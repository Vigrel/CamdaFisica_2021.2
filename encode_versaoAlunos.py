import matplotlib.pyplot as plt
import sys
import numpy as np
import sounddevice as sd
from suaBibSignal import *

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

NUMBER_FREQ = {
    0 : (1336, 941),
    1 : (1209, 697),
    2 : (1336, 697),
    3 : (1477, 697),
    4 : (1209, 770),
    5 : (1336, 770),
    6 : (1477, 770),
    7 : (1209, 852),
    8 : (1336, 852),
    9 : (1477, 852)    
}

def main():
    print("Inicializando encoder")
    
    

    #declare um objeto da classe da sua biblioteca de apoio (cedida)
    generator =  signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    freq_amostragem =  44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    
    duration = 5 
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3

    num_digitado = int(input("Digite o numero: "))
    print("Gerando Tons base")
    freq_num = NUMBER_FREQ[num_digitado]
    print(freq_num)
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 

    sin1, amp1 = generator.generateSin(freq_num[0], 0.25, duration, freq_amostragem)
    sin2, amp2 = generator.generateSin(freq_num[1], 0.25, duration, freq_amostragem)


    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    amp_soma = amp1 + amp2
    limites = [0,0.01,-1,1] 
    plt.axis(limites)
    plt.plot(sin1, amp_soma)
    plt.title('Frequencias somadas')
    plt.show()
    
    generator.plotFFT(amp_soma, freq_amostragem)

    #deixe tudo como array

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    print("Gerando Tom referente ao símbolo : {}".format(num_digitado))
    
    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    
    #printe o grafico no tempo do sinal a ser reproduzido
    # reproduz o som
    sd.play(amp_soma, freq_amostragem)
    # Exibe gráficos
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
