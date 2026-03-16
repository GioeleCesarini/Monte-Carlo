"""
1) Simulare utilizzando il metodo MonteCarlo la distribuzione dell'energia dei fotoni gamma emessi da un AGN (Active Galactic Nuclei) che segue una distribuzione:

 => F(E) = A * E^{- G}  => ( G = GAMMA)

    dove "E" è l'energia del fotone gamma e "G" è l'indice spettrale che vale: G = 1.8.
   
    L'energia dei fotoni gamma varia tra E_min = 10 e E_max = 100.
   
2) Simula inoltre la risposta di un rivelatore di energia di fotoni con una risoluzione in energia del 10%.

3) Si sovrappongano i due istogrammi ottenuti.
"""

import math as ma
from ROOT import TRandom3

from ROOT import TH1D, TCanvas, gApplication, TLegend

################
#== COSTANTI ==#
################

G = 1.8

# ============================ #
# Generatore di numeri casuali #
# ============================ #

rnd=TRandom3()
rnd.SetSeed(123456789)

'''==================
       PARTE 1
=================='''

# L'intento è quello di "disengare" un rettangolo sopra la curva: f(E), poi generare punti casuali dentro quel rettangolo e tenere solo quelli sotto la curva effettivamente.
# Immagina:
# - L'asse X rappresenta i valori possibili di "E" (tra 10 e 100).
# - L'asse Y va da 0 a f_E_Max = f(10).
# - Tu **generi punti casuali (E, y)** all'interno di questo rettangolo.
# - Tieni solo quelli **che cadono sotto la curva f(E)**.

# => Così facendo, la **densità di punti accettati** segue la forma della funzione f(E)!

f_E_Max = 10 ** (-G)

N = 10000

Energies = [] # => Inizializza una lista dove salveremo le energie dei fotoni accettati

# Ciclo monte-carlo
while len(Energies) < N: # => questo ciclo continua finché non si ha una lista con N elementi
    E = 10 + rnd.Rndm() * 90
    f_E = E ** (-G)
    y = rnd.Rndm() * f_E_Max # => Genero un numero casuale tra 0 e f_E_Max
    if y < f_E:
        Energies.append(E)

'''==================
       PARTE 2
=================='''

# Per simulare la risposta di un rivelatore è piuttosto semplice, bisogna perturbare ogni energia vera E con una distribuzione gaussiana, che simuli l’imprecisione del rivelatore. Cosa significa con una risoluzione dell'enerigia del 10%? Ovvero con:

EnergiesMisurate = []

for E in Energies:
    sigma = 0.1 * E
    E_misurata = rnd.Gaus(E, sigma)
    EnergiesMisurate.append(E_misurata)

# => gaussiana con media E e sigma il 10%

'''==================
       PARTE 3
=================='''

#===================#
# == Istogramma  == #
#===================#

h = TH1D("h", " ", 150, 0, 110)

for E in Energies:
    h.Fill(E)
    
c1 = TCanvas("c1", "Grafico", 800, 600)

c1.cd()  # Rende il canvas c1 attivo, da dopo questo comando tutto ciò che disegno sarà su c1

h.Draw("HIST") # disegni h sul canvas attivo
h.SetLineColor(2)  # rosso
h.SetTitle("Distribuzione teorica vs rilevatore ;Energia [MeV];Conteggi")

H = TH1D("H", " ", 150, 0, 110)

for E in EnergiesMisurate:
    H.Fill(E)

H.Draw("HIST SAME")
H.SetLineColor(4)  # blu

# LEGENDA #

legend = TLegend(0.6, 0.7, 0.88, 0.85) # => i numeri dentro sono solo la posizione nel grafico

# legend.AddEntry(obj, label, option)
# *) "obj" => l'istogramma o la curva
# *) "label" => la stringa da scrivere nella legenda
# *) "option" => che tipo di simbolo o linea usare: *) "l" = linea (per istogrammi o funzioni), *) "f" = area piena (fill, per istogrammi con area colorata), *) "p" = punto (marker), *) "lep" = linea e punto
legend.AddEntry(h, "Teorico", "l")
legend.AddEntry(H, "Misurato (rivelatore)", "l")
legend.Draw()

#=====================#

gApplication.Run(True)
