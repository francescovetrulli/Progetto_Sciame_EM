from Particella import Particella
from Fotone import Fotone
import random
import numpy as np

class Sciame:
	
	def __init__(self, E0, dE, s, Ec, segno = -1):
		'''
		Crea lo sciame elettromagnetico

		Parametri:
			E0(float): Energia iniziale [MeV]
			dE(float): Perdita per ionizzazione in una lunghezza di 
			radiazione [Mev]
			s(float): Passo della simulazione
			segno(int): Identifica la particella iniziale, -1 elettrone,
			 +1 positrone e 0 fotone, default = -1
		Attributi:
			t(int): Numero di passi eseguiti
			en_ionizzazione_step(list): Energia persa per ionizzazione 
			ad ogni step
			contatore(list): Numero di particelle presenti ad ogni step
			Ec(list): Energie critica del materiale per elettroni e 
			positroni [MeV] 
		'''
		
		if E0 < 0:
			raise ValueError("L'energia iniziale deve essere positiva")
		self.E0 = E0
		
		if dE < 0:
			raise ValueError("La perdita di energia per lunghezza di ionizzazione deve essere positiva ")
		self.dE = dE
		
		if Ec[0] < 0 or Ec[1] < 0 :
			raise ValueError("Le energie critiche devono essere positive")
		self.Ec = Ec
		
		if s <= 0 or s > 1 :
			raise ValueError("Il passo deve essere compreso tra 0 e 1")
		self.s = s
		
		if segno != -1 and segno != 0 and segno != 1 :
			raise ValueError("Il segno deve essere uno dei seguenti valori: (-1,0,+1)")
		self.segno = segno
		
		self.en_ionizzazione_step = []
		self.t = 0
		
		if segno == 0:
			prima = Fotone(E0)
		else:
			prima = Particella (E0, dE, s, segno)
			
		self.lista = [prima]
		self.contatore = [1]
	
	
	def step(self):
		'''
		Simula i passi dello sciame elettromagnetico, finché ci sono 
		particelle in grado di cedere energia. 

		Parametri:
			None
		Returns:
			None (modifica la lista delle particelle e, ad ogni passo, 
			salva il numero del passo, l'energia persa per ionizzazione
			e il numero di particelle presenti)
		'''
		
		p_emissione = 1 - np.exp( -self.s )
		p_coppie = 1 - np.exp( (- 7/9) * self.s )
		
		while len(self.lista) > 0:
				
			lista_nuova = []
			e_counter = 0
			
			for p in self.lista:
				
				if (type(p) == Particella):
				
					if (p.energia < p.energia_soglia):
					
						e_counter += p.energia * random.random()
						continue
					
					else:
						
						if (random.random() < p_emissione):
							
							if(p.segno == -1 and p.energia > self.Ec[0]):
								
								p.emissione(lista_nuova)
					
							elif(p.segno == +1 and p.energia > self.Ec[1]):
								
								p.emissione(lista_nuova)
								
						p.ionizzazione()
						e_counter += p.energia_soglia
						lista_nuova.append(p)
					
				elif (type(p) == Fotone):
						
					if (p.energia > 2 * 0.511) :
							
						if (random.random() < p_coppie):
								
							p.coppie(lista_nuova, self.dE, self.s)
							continue
							
						else:
							
							lista_nuova.append(p)
							
					else:
						
						e_counter += p.energia * random.random()
						continue
		
			self.lista = lista_nuova
			self.t += 1
			self.en_ionizzazione_step.append(e_counter)
			self.contatore.append(len(self.lista))
		
	def energia_totale(self):
		'''
		Calcola l'energia totale persa per ionizzazione

		Parametri:
			None
		Returns:
			e_tot(float): Energia totale persa per ionizzazione
		'''		
		e_tot = np.sum(self.en_ionizzazione_step)
		
		return e_tot
		
	
	

			
		
	
	
	
	
	
	
	
	
	
	
	
				
