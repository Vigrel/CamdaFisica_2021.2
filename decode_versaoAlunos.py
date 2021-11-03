#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from suaBibSignal import *
import time
import peakutils

#funcao para transformas intensidade acustica em dB
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
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)
    signal = signalMeu()    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    freq_amostragem = 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = freq_amostragem
    sd.default.channels = 2  
    duration = 3


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("Captação iniciara em 2 segundos")
    time.sleep(2)
   
   #faca um print informando que a gravacao foi inicializada
    print("Captação do som:")
   
   #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
   #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = freq_amostragem * duration
   
    audio = sd.rec(int(numAmostras), freq_amostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    print(audio)
    #grave uma variavel com apenas a parte que interessa (dados)
    dados = np.squeeze(audio)
    # # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(0,duration,numAmostras)

    # plot do gravico  áudio vs tempo!
    plt.plot(t, dados)
    plt.title('Frequencias somadas')
    plt.show()    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, freq_amostragem)
    limites = [0,1500, 0,1000] 
    plt.axis(limites)
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()

    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    index = peakutils.indexes(yf, thres=0.3, min_dist=50)
    print(index)
    
    # printe os picos encontrados! 
    numdigitadoY, numdigitadoX = xf[index[0]], xf[index[1]]
    print(f'seu numero é {list(NUMBER_FREQ.keys())[list(NUMBER_FREQ.values()).index((round(numdigitadoX), round(numdigitadoY)))]}') 

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    # ## Exibe gráficos 
    plt.show()

if __name__ == "__main__":
    main()
