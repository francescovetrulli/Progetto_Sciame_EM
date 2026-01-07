import numpy as np
import matplotlib.pyplot as plt
from Sciame_EM import Sciame
import argparse

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
    risultati[nome] = {"t": [], "t_err": [], "E": [], "E_err": []}

print(f"\nConfigurazione simulazione per: {list(materiali.keys())}:\n" 
      f"- Range energia: da 0 a {E_max} MeV\n" 
      f"- Numero di campioni energetici: {args.n}\n" 
      f"- Ripetizioni per valore di energia: {args.M}\n" 
      f"- Passo della simulazione: {args.s}\n")

for E in energie:
    for nome, dati in materiali.items():
        t_temp = []
        E_temp = []
        
        for i in range(args.M):
            s1 = Sciame(E, dati["dE"], args.s, dati["Ec"], args.segno)
            s1.step()
            t_temp.append(s1.t)
            E_temp.append(s1.energia_totale())
        

        risultati[nome]["t"].append(np.mean(t_temp))
        risultati[nome]["t_err"].append(np.std(t_temp) / np.sqrt(args.M))
        risultati[nome]["E"].append(np.mean(E_temp))
        risultati[nome]["E_err"].append(np.std(E_temp) / np.sqrt(args.M))


fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle(f"Simulazione di {args.n * args.M} sciami", fontsize=16)

for nome, dati in materiali.items():
    res = risultati[nome]
    X0 = dati["X0"]
    axes[0].errorbar(energie, np.array(res["t"]) * args.s * X0, yerr=np.array(res["t_err"]) * args.s * X0, color=dati["color"], label=nome, marker='o', alpha=0.7)
    axes[1].errorbar(energie, res["E"], yerr=res["E_err"], color=dati["color"], label=nome, marker='o', alpha=0.7)

axes[0].set_title("Distanza massima dello sciame", fontsize=14)
axes[0].set_ylabel("Distanza [cm]")
axes[1].set_title("Energia depositata dallo sciame", fontsize=14)
axes[1].set_ylabel("Energia depositata [MeV]")
axes[0].set_xlabel("Energia primaria [MeV]")
axes[1].set_xlabel("Energia primaria [MeV]")
axes[0].set_xscale('log') 
axes[1].set_xscale('log') 
axes[0].grid(True, linestyle='--', alpha=0.5)
axes[1].grid(True, linestyle='--', alpha=0.5)
axes[0].legend()
axes[1].legend()

plt.tight_layout()
plt.subplots_adjust(top=0.88)
plt.show()
