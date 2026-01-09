import matplotlib.pyplot as plt
from Sciame_EM import Sciame
import argparse
import numpy as np 

'''
SIMULAZIONE DI SCIAMI ELETTROMAGNETICI

Il codice esegue una simulazione di n sciami elettromagnetici partendo da 
una particella di energia E0. 
Calcola lo sviluppo longitudinale dello sciame, analizzando sia la 
composizione particellare che la deposizione energetica (dE/dx).

INPUT (argparse):

	E0(float): Energia della particella primaria [MeV]
	
	segno(int): Tipo di particella iniziale (1: e+, -1: e-, 0: gamma)
	
	s(float): Passo della simulazione in frazioni di X0
	
	dE(float): Perdita di energia per ionizzazione per unità di passo
	
	Ece, Ecp(float): Energie critiche per elettroni e positroni nel mezzo
	
	n(int): Numero di sciami per la media statistica
	
	X0(float): Lunghezza di radiazione del materiale [cm]

VARIABILI:

	sciami(list): Oggetti Sciame simulati
	
	E_totali(list): Energie totali depositate per ogni singolo sciame
	
	Num_totali, err(np.array): Numero medio finale di fotoni, elettroni e positroni con relativo errore sulla media
	
	d_max(float): Profondità media del picco dello sciame [cm]
	
	distanza(np.array): Coordinate spaziali lungo l'asse di sviluppo [cm]
	
	t_max(int): Numero massimo di passi di tutti gli sciami
	
	E_matrice(list (n x t_max)): Deposizioni energetiche 
	
	f, el, po_matrice (list (n x t_max)): Numero di particelle per ogni step e sciame
	
	E_medie, E_err(list): Medie di dE/dx ad ogni passo con relativo errore sulla media
	
	f, el, po_medie, err (list): Numero medio di particelle per ogni step con relativo errore sulla media
	
	E_cumulativa, err(list): Energia totale depositata con relativo errore sulla media

GRAFICI:

	Pannello 'a': Evoluzione del numero di fotoni, elettroni e positroni
	
	Pannello 'b': Deposito di energia (dE/dx) lungo lo sciame
	
	Pannello 'c': Energia totale depositata
'''

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
    
print(f"Avvio simulazione di {args.n} sciami")

sciami = []
E_totali = []
Num_totali = np.zeros(3)
d_max = 0


for i in range(args.n):
	
	s1 = Sciame(args.E0, args.dE, args.s, [args.Ece, args.Ecp], args.segno)
	s1.step()
	sciami.append(s1)
    
	E_totali.append(s1.energia_totale())
	Num_totali += np.array(s1.contatore_tot)
	d_max += np.argmax(np.array(s1.en_ionizzazione_step)) 

d_max = d_max * args.s * args.X0 / args.n
Num_totali = Num_totali / args.n

t_max = 0

for s in sciami:
	
	if (s.t > t_max):
		t_max = s.t

distanza = np.arange(t_max) * args.s * args.X0

E_matrice = np.zeros((args.n, t_max))
f_matrice = np.zeros((args.n, t_max))
el_matrice = np.zeros((args.n, t_max))
po_matrice = np.zeros((args.n, t_max))

for i in range(args.n):
	
    s = sciami[i]
    
    for j in range(s.t):
		
        E_matrice[i][j] = s.en_ionizzazione_step[j]
        f_matrice[i][j] = s.contatore_step[0][j]
        el_matrice[i][j] = s.contatore_step[1][j]
        po_matrice[i][j] = s.contatore_step[2][j]
        

E_medie = np.mean(E_matrice, axis=0)
E_err = np.std(E_matrice, axis=0) / np.sqrt(args.n)

f_medie = np.mean(f_matrice, axis=0)
f_err = np.std(f_matrice, axis=0) / np.sqrt(args.n)

el_medie = np.mean(el_matrice, axis=0)
el_err = np.std(el_matrice, axis=0) / np.sqrt(args.n)

po_medie = np.mean(po_matrice, axis=0)
po_err = np.std(po_matrice, axis=0) / np.sqrt(args.n)

E_media = np.mean(np.array(E_totali))
E_media_err = np.std(E_media) / np.sqrt(args.n)
 
Num_totali_err = [np.sqrt(Num_totali[0]), np.sqrt(Num_totali[1]), np.sqrt(Num_totali[2])] 

E_cumulativa = np.cumsum(E_medie)
E_err_cumulativa = np.sqrt(np.cumsum(np.array(E_err)**2))

layout = [['a'], ['b'], ['c']]

fig, axes = plt.subplot_mosaic(layout, figsize=(16, 9), sharex=True)
fig.suptitle(f"Simulazione di {args.n} sciami a {args.E0} MeV", fontsize=16, fontweight = 'bold')


axes['a'].errorbar(distanza, f_medie, yerr=f_err, color='gold', alpha=0.7, label='$\gamma$')
axes['a'].errorbar(distanza, el_medie, yerr=el_err, color='red', alpha=0.7, label='$e^-$')
axes['a'].errorbar(distanza, po_medie, yerr=po_err, color='blue', alpha=0.7, label='$e^+$')
axes['a'].grid(True, linestyle='--', alpha=0.5)
axes['a'].set_ylabel("N. di particelle", fontsize = '16', labelpad=20)
axes['a'].legend(loc='upper left')
testo_boxa = (
    f"Numero medio di particelle totali\n"
    f"$N_\gamma$: {Num_totali[0]:} $\pm$ {Num_totali_err[0]:.2f}\n"
    f"$N_{{e^-}}$: {Num_totali[1]:} $\pm$ {Num_totali_err[1]:.2f}\n"
    f"$N_{{e^+}}$: {Num_totali[2]:} $\pm$ {Num_totali_err[2]:.2f}"
)
axes['a'].text(0.95, 0.95, testo_boxa, transform=axes['a'].transAxes, 
             verticalalignment='top', horizontalalignment='right', 
             fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
axes['a'].axvline(x=d_max, color='gray', linestyle='--', linewidth=1.5)

axes['b'].errorbar(distanza, E_medie, yerr=E_err, color='green', alpha=0.7)
axes['b'].grid(True, linestyle='--', alpha=0.5)
axes['b'].set_ylabel("dE / dx [MeV]", fontsize = '16', labelpad=20)
axes['b'].axvline(x=d_max, color='gray', linestyle='--', linewidth=1.5)

axes['c'].errorbar(distanza, E_cumulativa, yerr=E_err_cumulativa, color='purple', alpha=0.7, label='Energia cumulata')
axes['c'].grid(True, linestyle='--', alpha=0.5)
axes['c'].set_xlabel("Distanza [cm]", fontsize=16)
axes['c'].set_ylabel("$E_{TOT}$ [MeV]", fontsize = '16', labelpad=10)
axes['c'].axhline(y=args.E0, color='black', linestyle='--', linewidth=1.5, label=rf'Energia iniziale $E_0$')
testo_boxc = (
	f"$E_0$: {args.E0} MeV\n"
	f"$E_{{TOT}}$ media: {E_media:.1f} $\pm$ {E_media_err:.1f} MeV")
axes['c'].text(0.95, 0.05, testo_boxc, transform=axes['c'].transAxes, 
             verticalalignment='bottom', horizontalalignment='right', 
             fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
axes['c'].legend(loc='upper left')
axes['c'].axvline(x=d_max, color='gray', linestyle='--', linewidth=1.5)

plt.tight_layout()
fig.subplots_adjust(hspace=0.15)
plt.show()

