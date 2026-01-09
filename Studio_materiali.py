import numpy as np
import matplotlib.pyplot as plt
from Sciame_EM import Sciame
import argparse

'''
SIMULAZIONE DI SCIAMI ELETTROMAGNETICI NEI MATERIALI PER DIVERSE ENERGIE

Il codice simula sciami elettromagnetici per diverse energie in diversi 
materiali. 
Per ogni valore di energia, vengono effettuate ripetizioni statistiche 
per calcolare medie ed errori delle grandezze caratteristiche.

INPUT (argparse):

	n(int): Numero di campioni energetici 
	
	b(int): Ordine di grandezza per l'energia massima (k *10^b)
	
	k(float): Moltiplicatore per l'energia massima (k *10^b)
	
	s(float): Passo della simulazione in frazioni di X0
	
	M(int): Numero di ripetizioni statistiche per ogni punto di energia
	
	segno(int): Particella iniziale (-1: e-, 0: gamma, 1: e+)

VARIABILI:

	E_max (float): Energia massima del range di simulazione [MeV]
	
	energie (np.array): Vettore delle energie iniziali del campionamento [MeV]
	
	materiali (dict): Parametri fisici dei mezzi (dE, X0, Ec) e colore per i grafici
	
	risultati (dict): Risultati medi e relativi errori sulla media:
	
		"d", "d_err" (list): Distanza finale media di stop [cm]
		
		"E_tot", "E_tot_err" (list): Energia totale depositata media [MeV]
		
		"num_tot", "num_tot_err" (list): Numero medio di particelle nello sciame [gamma, e-, e+]
		
		"d_max", "d_max_err" (list): Distanza media del picco di deposizione [cm]
		
		"E_max_tot", "E_max_tot_err" (list): Valore medio dell'energia depositata al picco [MeV/cm]
		
		"num_max_tot", "num_max_tot_err" (list): Numero medio di particelle al picco [gamma, e-, e+]


	d_temp (list): Distanze di stop per ogni ripetizione statistica
		
	E_tot_temp (list): Energie totali depositate per ogni ripetizione statistica
		
	num_tot_temp (np.array): Particelle totali per ogni valore di energia
		
	d_max_temp (list): Distanze del picco per ogni ripetizione statistica
		
	E_max_temp (list): Deposito energetico massimo per ogni ripetizione statistica
		
	num_max_temp (list): Numero di particelle al picco per ogni ripetizione statistica
		
	idmax (int): Indice spaziale corrispondente al picco per ogni ripetizione statistica

	mat_p, mat_e (np.array): Composizione totale media con relativo errore sulla media 
		
	mat_m, mat_me (np.array): Composizione al picco media con relativo errore sulla media
		
	col (str): Colore associato al materiale

GRAFICI:

	Pannello 1 (Statistiche Totali): Distanza media di stop e energia totale depositata vs E0
	
	Pannello 2 (Composizione Totale): Numero totale di particelle prodotte vs E0
	
	Pannello 3 (Statistiche al Massimo): Profondità del picco (d_max) e valore del picco (dE/dx)_max vs E0
	
	Pannello 4 (Composizione al Massimo): Numero di particelle per tipo al picco vs E0
'''

parser = argparse.ArgumentParser(description="Simulazione di sciami elettromagnetici nei materiali")
parser.add_argument("n", type=int, help="Numero di campioni (energie)")
parser.add_argument("b", type=int, help="Ordine di grandezza energia massima (k*10^b)")
parser.add_argument("k", type=float, help="Moltiplicatore energia massima (k*10^b)")
parser.add_argument("s", type=float, help="Passo della simulazione")
parser.add_argument("M", type=int, help="Ripetizioni statistiche")
parser.add_argument("segno", type=int, choices=[-1,0,1], help="Segno particella iniziale")
args = parser.parse_args()

E_max = args.k * 10**args.b
energie = np.logspace(0, np.log10(E_max), args.n) 

materiali = {
	"Ice": {"dE": 1.822, "X0": 39.31, "Ec": [78.60, 76.50], "color": "blue"},
	"Concrete": {"dE": 3.935, "X0": 11.55, "Ec": [49.90, 48.50], "color": "gray"}
}

risultati = {}
for nome in materiali:
	risultati[nome] = {
	
		"d": [], "d_err": [], 
		"E_tot": [], "E_tot_err": [], 
		"num_tot": [], "num_tot_err": [], 
		"d_max": [], "d_max_err": [], 
		"E_max_tot": [], "E_max_tot_err": [], 
		"num_max_tot": [], "num_max_tot_err": [] 
	}

print(f"\nConfigurazione simulazione per: {list(materiali.keys())}:\n" 
	f"- Range energia: da 0 a {E_max} MeV\n" 
	f"- Numero di campioni energetici: {args.n}\n" 
	f"- Ripetizioni per valore di energia: {args.M}\n" 
	f"- Passo della simulazione: {args.s}\n")

for E in energie:
	for nome, dati in materiali.items():
		
		d_temp = []
		E_tot_temp = []
		num_tot_temp = np.zeros(3)
		
		d_max_temp = []
		E_max_temp = []
		num_max_temp = []
		
		for i in range(args.M):
			
			s1 = Sciame(E, dati["dE"], args.s, dati["Ec"], args.segno)
			s1.step()
			
			d_temp.append(s1.t * args.s * dati["X0"])
			E_tot_temp.append(s1.energia_totale())
			num_tot_temp += np.array(s1.contatore_tot)
			
			idmax = np.argmax(s1.en_ionizzazione_step)
			d_max_temp.append(idmax * args.s * dati["X0"])
			E_max_temp.append(s1.en_ionizzazione_step[idmax])
			num_max_temp.append([s1.contatore_step[0][idmax], s1.contatore_step[1][idmax], s1.contatore_step[2][idmax]])
		
		risultati[nome]["d"].append(np.mean(d_temp))
		risultati[nome]["d_err"].append(np.std(d_temp) / np.sqrt(args.M))
		
		risultati[nome]["E_tot"].append(np.mean(E_tot_temp))
		risultati[nome]["E_tot_err"].append(np.std(E_tot_temp) / np.sqrt(args.M))
		
		risultati[nome]["num_tot"].append(num_tot_temp / args.M)
		risultati[nome]["num_tot_err"].append(np.sqrt(num_tot_temp) / args.M)

		risultati[nome]["d_max"].append(np.mean(d_max_temp))
		risultati[nome]["d_max_err"].append(np.std(d_max_temp) / np.sqrt(args.M))
		
		risultati[nome]["E_max_tot"].append(np.mean(E_max_temp))
		risultati[nome]["E_max_tot_err"].append(np.std(E_max_temp) / np.sqrt(args.M))
		
		risultati[nome]["num_max_tot"].append(np.mean(num_max_temp, axis=0))
		risultati[nome]["num_max_tot_err"].append(np.std(num_max_temp, axis=0) / np.sqrt(args.M))

fig1, ax1 = plt.subplots(2, 1, figsize=(10, 12), sharex=True)
fig1.suptitle("Statistiche Totali dello Sciame", fontsize=16, fontweight='bold')

for nome, d_mat in risultati.items():
	col = materiali[nome]["color"]
	
	ax1[0].errorbar(energie, d_mat["d"], yerr=d_mat["d_err"], label=nome, color=col, marker='o')
	ax1[0].set_ylabel("${d_{STOP}}$ [cm]", fontsize=16, labelpad=20)
	
	ax1[1].errorbar(energie, d_mat["E_tot"], yerr=d_mat["E_tot_err"], label = nome, color=col, marker='o')
	ax1[1].set_ylabel("$E_{TOT}$ [MeV]", fontsize = '16', labelpad=20)
	
ax1[1].set_xlabel("Energia iniziale $E_0$ [MeV]", fontsize = '16')

for a in ax1: 
	
	a.grid(True, linestyle='--')
	a.legend(loc='upper left', fontsize='small')
	a.set_xscale('log')
	
plt.tight_layout()
plt.show() 


fig2, ax2 = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
fig2.suptitle("Composizione totale dello sciame", fontsize=16, fontweight='bold')

for nome, d_mat in risultati.items():
	col = materiali[nome]["color"]

	mat_p = np.array(d_mat["num_tot"])
	mat_e = np.array(d_mat["num_tot_err"])
	
	ax2[0].errorbar(energie, mat_p[:, 0], yerr=mat_e[:, 0], label=f"$\gamma$ {nome}", color=col, ls='-', marker='o')
	ax2[1].errorbar(energie, mat_p[:, 1], yerr=mat_e[:, 1], label=f"$e^-$ {nome}", color=col, ls='-', marker='s')
	ax2[2].errorbar(energie, mat_p[:, 2], yerr=mat_e[:, 2], label=f"$e^+$ {nome}", color=col, ls='-', marker='^')
	
	ax2[0].set_ylabel(f"N. $\gamma$ totali", fontsize = '16', labelpad=20)
	ax2[1].set_ylabel(f"N. $e^-$ totali", fontsize = '16', labelpad=20)
	ax2[2].set_ylabel(f"N. $e^+$ totali", fontsize = '16', labelpad=20)

ax2[2].set_xlabel("Energia iniziale $E_0$ [MeV]",fontsize = '16')
	
for a in ax2: 
	
		a.grid(True, linestyle='--')
		a.legend(loc='upper left', fontsize='small', ncol=2)
		a.set_xscale('log')
		
plt.tight_layout()
plt.show() 

fig3, ax3 = plt.subplots(2, 1, figsize=(10, 12), sharex=True)
fig3.suptitle("Statistiche al picco dello Sciame", fontsize=16, fontweight='bold')

for nome, d_mat in risultati.items():
	col = materiali[nome]["color"]
	
	ax3[0].errorbar(energie, d_mat["d_max"], yerr=d_mat["d_max_err"], label=nome, color=col, marker='o')
	ax3[0].set_ylabel("$d_{max}$ [cm]", fontsize = '16', labelpad=20)
	
	ax3[1].errorbar(energie, d_mat["E_max_tot"], yerr=d_mat["E_max_tot_err"], label=nome, color=col, marker='s')
	ax3[1].set_ylabel("$(dE/dx)_{max}$ [MeV/cm]", fontsize = '16', labelpad=20)
	
for a in ax3: 
	
	a.grid(True, linestyle='--', alpha=0.6)
	a.legend(loc='upper left', fontsize='small')
	a.set_xscale('log')
	
ax3[1].set_xlabel("Energia iniziale $E_0$ [MeV]", fontsize = '16')
plt.tight_layout()
plt.show()


fig4, ax4 = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
fig4.suptitle("Composizone al picco dello Sciame", fontsize=16, fontweight='bold')

for nome, d_mat in risultati.items():
	col = materiali[nome]["color"]

	mat_m = np.array(d_mat["num_max_tot"])
	mat_me = np.array(d_mat["num_max_tot_err"])
	
	ax4[0].errorbar(energie, mat_m[:, 0], yerr=mat_me[:, 0], label=f"$\gamma$ {nome}", color=col, ls='-', marker='o')
	ax4[1].errorbar(energie, mat_m[:, 1], yerr=mat_me[:, 1], label=f"$e^-$ {nome}", color=col, ls='-', marker='s')
	ax4[2].errorbar(energie, mat_m[:, 2], yerr=mat_me[:, 2], label=f"$e^+$ {nome}", color=col, ls='-', marker='^')
	
	ax4[0].set_ylabel(f"N. $\gamma$ totali", fontsize = '16', labelpad=20)
	ax4[1].set_ylabel(f"N. $e^-$ totali", fontsize = '16', labelpad=20)
	ax4[2].set_ylabel(f"N. $e^+$ totali", fontsize = '16', labelpad=20)
	
	
ax4[2].set_xlabel("Energia iniziale $E_0$ [MeV]", fontsize = '16')
	
for a in ax4: 
	
	a.grid(True, linestyle='--', alpha=0.6)
	a.legend(loc='best', fontsize='small', ncol=2)
	a.set_xscale('log')

plt.tight_layout()
plt.show()
