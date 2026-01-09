class Particella:

	def __init__(self, energia, dE, s, segno):
		'''
		Crea una particella.

		Parametri:
		
			energia(float) : Energia della particella
			
			dE(float): Perdita per ionizzazione in una lunghezza di 
			radiazione [Mev]
			
			s(float): Passo della simulazione in frazioni di lunghezza 
			di radiazione
			
			segno(int) : +1 per positroni, -1 per elettroni
			
		Attributi:
		
			energia_soglia(float): Energia minima per ionizzare, 
			è l'energia persa per ionizzazione in uno step [MeV]
		'''
		self.energia = energia
		self.energia_soglia = dE * s
		self.segno = segno

	def emissione(self, sciame):
		'''
		Simula il Bremsstrahlung dell'elettrone.

		Parametri:
		
			sciame(list): Particelle  presenti nello sciame
			
		Returns:
		
			None: Aggiunge a sciame un fotone con metà energia e modifica
			l'energia della particella
		'''
		
		from Fotone import Fotone
		nuova_energia = self.energia / 2
		self.energia = nuova_energia
		sciame.append(Fotone(nuova_energia))
		
	def ionizzazione(self):
		'''
		Simula la perdita di energia per ionizzazione.

		Parametri:
		
			None
			
		Returns:
		
			None: Modifica l'energia della particella sottraendo 
			l'energia di soglia
		'''
		self.energia -= self.energia_soglia




    
