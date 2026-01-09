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
			
			Ec(list): Energie critica del materiale per elettroni 
			(Ec[0]) e positroni (Ec[1]) [MeV]
			
			segno(int): Identifica la particella iniziale, -1 elettrone,
			 +1 positrone e 0 fotone, default = -1
			 
		Attributi:
		
			t(int): Numero di passi totali eseguiti
			
			en_ionizzazione_step(list): Energia persa per ionizzazione 
			ad ogni step
			
			contatore_tot (list): Numero di particelle totali 
			prodotte dallo sciame divise per tipo ([0] = fotoni, 
			[1] = elettroni, [2] = positroni)
			
			contatore_step (list): Numero di particelle totali 
			ad ogni step per tipo ([0] = fotoni, [1] = elettroni, 
			[2] = positroni), dimensione (3, t)
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
		
		self.contatore_tot = [0,0,0]
		self.contatore_step = [[],[],[]]
		
		if segno == 0:
			
			prima = Fotone(E0)
			self.contatore_tot[0] += 1
			
		else:
			
			prima = Particella (E0, dE, s, segno)
			
		
			if (segno == -1):
				
				self.contatore_tot[1] += 1
				
			else :
				
				self.contatore_tot[2] += 1 
			
		self.lista = [prima]
				
	def step(self):
		'''
		Simula i passi dello sciame elettromagnetico, finché ci sono 
		particelle in grado di cedere energia. 

		Parametri:
		
			None
			
		Attributi modificati:
		
			t(int): Incrementa il numero di passi totali eseguiti
			
			en_ionizzazione_step(list): Aggiunge l'energia persa per 
			ionizzazione ad ogni step
			
			contatore_tot(list): Aggiorna il numero totale di particelle 
			prodotte nello sciame per tipo
			
			contatore_step(list): Aggiunge il numero di particelle presenti 
			per tipo ad ogni step
			
			lista(list): Aggiorna l'elenco delle particelle attive 
			nello sciame
			
		Returns:
		
			None: Modifica la lista delle particelle e, ad ogni passo, 
			salva il numero del passo, l'energia persa per ionizzazione
			e il numero di particelle presenti per tipo.
		'''
		
		p_emissione = 1 - np.exp( -self.s )
		p_coppie = 1 - np.exp( (- 7/9) * self.s )
		
		while len(self.lista) > 0:
				
			lista_nuova = []
			en_contatore = 0
			f_contatore, el_contatore, po_contatore = 0, 0, 0
			
			for p in self.lista:
				
				if (type(p) == Particella):
				
					if(p.segno == -1):
						
						el_contatore += 1
					
					else:
						
						po_contatore +=1
					
					if (p.energia < p.energia_soglia):
					
						en_contatore += p.energia * random.random()
						continue
					
					else:
						
						if (random.random() < p_emissione):
							
							if((p.segno == -1 and p.energia > self.Ec[0]) or (p.segno == +1 and p.energia > self.Ec[1])):
								
								p.emissione(lista_nuova)
								self.contatore_tot[0] +=1
								
						p.ionizzazione()
						en_contatore += p.energia_soglia
						lista_nuova.append(p)
					
				elif (type(p) == Fotone):
					
					f_contatore += 1
						
					if (p.energia > 2 * 0.511):
							
						if (random.random() < p_coppie):
								
							p.coppie(lista_nuova, self.dE, self.s)
							
							self.contatore_tot[1] += 1
							self.contatore_tot[2] += 1
							continue
							
						else:
							
							lista_nuova.append(p)
							
					else:
						
						en_contatore += p.energia * random.random()
						continue
		
			self.lista = lista_nuova
			self.t += 1
			self.en_ionizzazione_step.append(en_contatore)
			self.contatore_step[0].append(f_contatore)
			self.contatore_step[1].append(el_contatore)
			self.contatore_step[2].append(po_contatore)
		
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
		
	
	

			
		
	
	
	
	
	
	
	
	
	
	
	
				
