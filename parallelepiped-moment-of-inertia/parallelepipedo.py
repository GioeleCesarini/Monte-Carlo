#================#
 #====Teoria====#  # => Prima di iniziare vediamo alcuni punti sulla teoria dietro all'eserzio
#================#

# MOMENTO DI INERZIA #
# Il momento di ineriza si calcola nel seguente modo:
# => I = int_V rho(\va{r}) * r^2 * dV
# dove: *) rho(\va{r}) -> densità nel punto \va{r}
#       *) r -> è la distanza tra il punto r e l'asse di rotazione
#       *) dV -> è l'elemento di volume

# CASO 1
# => rho(\va{r}) = rho_0 = 3
# => Asse di rotazione: passante per un estremo → tipicamente si intende lungo uno spigolo, per esempio l’asse z => da (0,0,0) a (0,0,c)
# => I = int_V rho(\va{r}) * r^2 * dV = I = int_V rho_0 * (x^2 + y^2)  * dV = 3 * int_V (x^2 + y^2)  * dV
# => poiché la distanza è: r^2 = x^2 + y^2 + z^2 ma sull'asse z (z = 0), vale: r = x^2 + y^2
# Allora abbiamo ottenuto:
# => I = 3 * int_V (x^2 + y^2) * dV = abc * (a^2 + b^2) = I_{teorico} => lo usiamo per verificare il risultato
# Ma nella pratica?
# Per un solido di cui bisogna calcolare il volume è chiaro il ragionamento, monte carlo conta quanti punti cadono all'interno del solido. Ma in questo caso è leggermente diverso poiché non vogliamo il volume bensì il momento di inerzia, allora sappi che in generale per un integrale del tipo:
# -> int_V f(r) dV, monte carlo ci aiuta ad approssimarlo come somma del tipo: V/N * sum_{i = 0}^{i = N} f(r_i) => possiamo dire che l’approccio base del metodo Monte Carlo: si approssima un integrale come media di campioni moltiplicata per il volume.
# Allora nel nostro caso: 3V/N * sum_{i = 0}^{i = N} (x^2 + y^2), quindi nel ciclo mettiamo la somma, fuori dal ciclo moltiplicheremo la somma per 3V/N, con 3 = rho0
#=====================#

import math as ma
from ROOT import TRandom3

################
#== COSTANTI ==#
################

a = 4
b = 2
c = 3

rho0 = 3

# ============================ #
# Generatore di numeri casuali #
# ============================ #

rnd=TRandom3()
rnd.SetSeed(123456789)

# Volume parallelepipedo
V = a * b * c

# Numero di punti monte carlo
N = 10000

# Variabile per accumulare la somma:

sommaMC = 0 # => per cacolare I_MC
sommaMC2 = 0 # => per calcolare l'errore statistico

# Ciclo monte-carlo
for i in range(N):
    x = rnd.Rndm() * a
    y = rnd.Rndm() * b
    z = rnd.Rndm() * c
    # Ricordo che il metodo: rnd.Rndm() randomizza un numero tra 0 ed 1, escluso 0
     
    # Distanza dall'asse z
    r2 = x**2 + y**2
    
    sommaMC += r2
    sommaMC2 += r2**2

I_MC = rho0 * V/N * sommaMC

#==================#
#--VALORE TEORICO--#
#==================#

I_t = a * b * c * (a**2 + b**2)

#==================#
#----- ERRORS -----#
#==================#

# Dalla teoria so:
# Presa una funz: f_i = x**2 + y**2
# La media è:
# => fMed = 1/N * sum_{1}^{N} f_i     e    (f^2)Med = 1/N * sum_{1}^{N} f^2_i    ==> Per questo salvo anche gli f^2
# La varianza è: => Var = 1/N * ( (f^2)Med - (fMed)^2 )
# La dev standard sarà infine: rho0 * V * sqrt{ Var }

media = sommaMC/N
media2 = sommaMC2/N
varianza = media2 - media**2

erroreMC = rho0 * V * ma.sqrt( varianza/N ) # Ricorda infatti che l'errore sulla media è la radice della varianza ma l'errore sul campionamento I va pesato per rho0 e V

#==================#
#----- STAMPA -----#
#==================#

print(f"Stima Monte Carlo: I = {I_MC:.2f} ± {erroreMC:.2f}")
print(f"Valore teorico atteso: I = {I_t:.2f}")

scostamento = abs(I_MC - I_t)
print(f"Scostamento assoluto: {scostamento:.2f}")

# Quanto è significativo lo scostamento?
if scostamento < 2 * erroreMC:
    print("✅ La stima Monte Carlo è compatibile con il valore teorico (entro 2σ)")
else:
    print("⚠️ La stima NON è compatibile con il valore teorico (oltre 2σ)")

sommaMC_NEW_x = 0

sommaMC_NEW_z = 0

# Ciclo monte-carlo
for i in range(N):
    x = rnd.Rndm() * a
    y = rnd.Rndm() * b
    z = rnd.Rndm() * c
    
    rho = rho0 * x / a # In zero vale "0", in "a" vale rho0
    
    sommaMC_NEW_x += rho * (z**2 + y**2)
    sommaMC_NEW_z += rho * (x**2 + y**2)

I_MC_NEW_x = V/N * sommaMC_NEW_x
I_MC_NEW_z = V/N * sommaMC_NEW_z

print(f"Stima Monte Carlo nel caso di densità variabile rispetto x: I = {I_MC_NEW_x:.2f}")
print(f"Stima Monte Carlo nel caso di densità variabile rispetto z: I = {I_MC_NEW_z:.2f}")
