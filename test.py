import matplotlib.pyplot as plt
from Sciame_EM import Sciame
import argparse
import numpy as np 

parser = argparse.ArgumentParser(description="Sciame elettromagnetico")
parser.add_argument("E0", type=float, help="Energia della particella iniziale")
parser.add_argument("segno", type=int, choices=[-1,0,1], help="Segno della particella iniziale")
parser.add_argument("s", type=float, help="Passo della simulazione")
parser.add_argument("dE", type=float, help="Perdita per ionizzazione [MeV]")
parser.add_argument("Ece", type=float, help="Energia critica elettrone [MeV]")
parser.add_argument("Ecp", type=float, help="Energia critica positrone [MeV]")
parser.add_argument("n", type=int, help="Numero di sciami da simulare")
parser.add_argument("X0", type=float, help="Lunghezza di radiazione [cm]")
args = parser.parse_args()
    
print(f"Avvio simulazione di {args.n} sciami...")

sciami = []
E_totali = []

for i in range(args.n):
    s1 = Sciame(args.E0, args.dE, args.s, [args.Ece, args.Ecp], args.segno)
    s1.step()
    sciami.append(s1)
    E_totali.append(s1.energia_totale())

t_max = 0

for s in sciami:
	
	if (len(s.contatore) > t_max):
		t_max = len(s.contatore)

distanza = np.arange(t_max) * args.s * args.X0

E_matrice = np.zeros((args.n, t_max))
N_matrice = np.zeros((args.n, t_max))

for i in range(len(sciami)):
    s = sciami[i]
    
    for j in range(len(s.en_ionizzazione_step)):
        E_matrice[i][j] = s.en_ionizzazione_step[j]
        
    for j in range(len(s.contatore)):
        N_matrice[i][j] = s.contatore[j]

E_medie = np.mean(E_matrice, axis=0)
N_medie = np.mean(N_matrice, axis=0)
E_err = np.std(E_matrice, axis=0) / np.sqrt(args.n)
N_err = np.std(N_matrice, axis=0) / np.sqrt(args.n)

E_media = np.mean(np.array(E_totali))
Ec_media = (args.Ece + args.Ecp) / 2
fig, axes = plt.subplots(1, 2, figsize=(14,5)) 
fig.suptitle(f"Simulazione di {args.n} sciami", fontsize=16)

axes[0].errorbar(distanza, N_medie, yerr=N_err, color='blue', alpha=0.7)
axes[0].grid(True, linestyle='--', alpha=0.5)
axes[0].set_title("Sviluppo longitudinale", fontsize=14)
axes[0].set_xlabel("Distanza [cm]", fontsize=12)
axes[0].set_ylabel("Numero medio di particelle", fontsize=12)


axes[1].errorbar(distanza, E_medie, yerr=E_err, color='red', alpha=0.7)
axes[1].grid(True, linestyle='--', alpha=0.5)
axes[1].set_title("Deposito di energia per ionizzazione", fontsize=14)
axes[1].set_xlabel("Distanza [cm]", fontsize=12)
axes[1].set_ylabel("Energia [MeV]", fontsize=12)
testo_box = (f"Energia Iniziale ($E_0$): {args.E0} MeV\n" f"Energia Totale Depositata: {E_media:.1f} MeV\n")
axes[1].text(0.95, 0.95, testo_box, transform=axes[1].transAxes, verticalalignment='top', horizontalalignment='right', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()
