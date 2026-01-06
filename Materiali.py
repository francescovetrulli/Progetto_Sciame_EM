import numpy as np
import matplotlib.pyplot as plt
from Sciame_EM import Sciame
import argparse

parser = argparse.ArgumentParser(description="Simulazione di sciami elettromagnetici")
parser.add_argument("n", type=int, help="Numero di campioni (energie) da analizzare nell'intervallo [0, 10^b] MeV")
parser.add_argument("b", type=int, help="Ordine di grandezza dell'energia massima: E_max = 10^b MeV")
parser.add_argument("s", type=float, help="Passo spaziale della simulazione (in unità di lunghezze di radiazione X0)")
parser.add_argument("M", type=int,help="Numero di ripetizioni statistiche per ogni singolo valore di energia")
parser.add_argument("segno", type=int,choices = [-1,0,1],help="Segno della particella che inizia lo sciame, -1 per elettrone, 0 per fotone e 1 per positrone")
args = parser.parse_args()

E_max = 10**args.b

print(f"\nConfigurazione simulazione:\n" 
      f"- Range energia: da 0 a {E_max} MeV (10^{args.b})\n" 
      f"- Numero di campioni energetici: {args.n}\n" 
      f"- Ripetizioni per valore di energia: {args.M}\n" 
      f"- Passo della simulazione: {args.s}\n")
energie = np.logspace(0, args.b, args.n) 

dE_ice = 1.822					#MeV
X0_ice = 39.31					#cm	
Ec_ice = [78.60, 76.50]			#Mev

dE_concrete = 3.935				#Mev
X0_concrete = 11.55				#cm
Ec_concrete = [49.90, 48.50]	#Mev

s_ice = []
s_concrete = []

t_ice = []
t_ice_err = []
t_concrete = []
t_concrete_err = []

E_ice = []
E_ice_err = []
E_concrete = []
E_concrete_err = []

for E in energie: 
	
	t_ice_n = []
	E_ice_n = []
	t_concrete_n = []
	E_concrete_n = []
	for i in range(args.M):
		
		sciame_ice = Sciame(E, dE_ice, args.s, Ec_ice, args.segno)
		sciame_ice.step()
		t_ice_n.append(sciame_ice.t)
		E_ice_n.append(sciame_ice.energia_totale())
		
		sciame_concrete = Sciame(E, dE_concrete, args.s, Ec_concrete, args.segno)
		sciame_concrete.step()
		t_concrete_n.append(sciame_concrete.t)
		E_concrete_n.append(sciame_concrete.energia_totale())
		
	t_ice.append(np.mean(t_ice_n))
	t_ice_err.append(np.std(t_ice_n) / np.sqrt(args.M))
	
	E_ice.append(np.mean(E_ice_n))
	E_ice_err.append(np.std(E_ice_n) / np.sqrt(args.M))
	
	t_concrete.append(np.mean(t_concrete_n))
	t_concrete_err.append(np.std(t_concrete_n) / np.sqrt(args.M))
	
	E_concrete.append(np.mean(E_concrete_n))
	E_concrete_err.append(np.std(E_concrete_n) / np.sqrt(args.M))


fig, axes = plt.subplots(1, 2, figsize=(14,5)) 

axes[0].errorbar(energie, np.array(t_ice) * args.s * X0_ice, yerr=np.array(t_ice_err) * args.s * X0_ice, color='blue', marker='o', linestyle='-', linewidth=2, alpha=0.8, label='Ice')
axes[0].errorbar(energie, np.array(t_concrete) * args.s * X0_concrete, yerr=np.array(t_concrete_err) * args.s * X0_concrete, color='gray', marker='s', linestyle='--', linewidth=2, alpha=0.8, label='Concrete')
#axes[0].set_xscale('log')  # utile se l'energia varia su più ordini di grandezza
axes[0].grid(True, linestyle='--', alpha=0.5)
axes[0].set_title("Sviluppo longitudinale dello sciame", fontsize=14)
axes[0].set_xlabel("Energia primaria [MeV]", fontsize=12)
axes[0].set_ylabel("Distanza longitudinale [cm]", fontsize=12)
axes[0].legend(fontsize=10)

axes[1].errorbar(energie, np.array(E_ice), yerr=np.array(E_ice_err), color='blue', marker='o', linestyle='-', linewidth=2, alpha=0.8, label='Ice')
axes[1].errorbar(energie, np.array(E_concrete), yerr=np.array(E_concrete_err), color='gray', marker='s', linestyle='--', linewidth=2, alpha=0.8, label='Concrete')
#axes[1].set_xscale('log')
axes[1].grid(True, linestyle='--', alpha=0.5)
axes[1].set_title("Energia depositata nello sciame", fontsize=14)
axes[1].set_xlabel("Energia primaria [MeV]", fontsize=12)
axes[1].set_ylabel("Energia depositata [MeV]", fontsize=12)
axes[1].legend(fontsize=10)

plt.tight_layout()
plt.show()




