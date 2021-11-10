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

arquivo, _ = sf.read("camFis.wav")
amplitude_max = np.max(np.abs(arquivo))
arquivo_norm = arquivo / amplitude_max

arquivo_filtrado = LPF(arquivo_norm, 4e3, taxa)

sd.play(arquivo_filtrado)
sd.wait()

tempo = len(arquivo) / taxa
portadora_t, portadora_y = signal.generateSin(14e3, 1, tempo, taxa)

sinal_modulado = portadora_y * arquivo_filtrado

sd.play(sinal_modulado)
sd.wait()

sf.write("arquivo_modulado.wav", sinal_modulado, taxa)

# Gráfico 1: Sinal de áudio original normalizado – domínio do tempo
plot_graph(arquivo_norm, "Sinal de áudio original normalizado – domínio do tempo")

# Gráfico 2: Sinal de áudio filtrado – domínio do tempo
plot_graph(arquivo_filtrado, "Sinal de áudio filtrado – domínio do tempo")

# Gráfico 3: Sinal de áudio filtrado – domínio da frequência
signal.plotFFT(arquivo_filtrado, taxa)

# Gráfico 4: Sinal de áudio modulado – domínio do tempo
plot_graph(sinal_modulado, "Sinal de áudio modulado – domínio do tempo")

# Gráfico 5: sinal de áudio modulado – domínio da frequência
signal.plotFFT(sinal_modulado, taxa)
