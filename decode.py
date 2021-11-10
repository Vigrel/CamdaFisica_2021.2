import numpy as np
import sounddevice as sd
import soundfile   as sf
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal
from suaBibSignal import signalMeu
from funcoes_LPF import *

signal = signalMeu()
taxa = 44100

sd.default.samplerate = taxa
sd.default.channels = 1

arquivo, _ = sf.read("arquivo_modulado.wav")

tempo = len(arquivo) / taxa

portadora_t, portadora_y = signal.generateSin(14e3, 1, tempo, taxa)

sinal_demodulado =  arquivo / portadora_y

arquivo_filtrado = LPF(sinal_demodulado, 4e3, taxa)

sd.play(arquivo_filtrado)
sd.wait()

# Gráfico 6: sinal de áudio demodulado – domínio da frequência
signal.plotFFT(sinal_demodulado, taxa)

# Gráfico 7: sinal de áudio demodulado e filtrado – domínio da frequência
signal.plotFFT(arquivo_filtrado, taxa)
