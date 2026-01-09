class Fotone:
	
	def __init__(self, energia):
		'''
		Crea un fotone.

		Parametri:
		
			energia(float) : Energia del fotone
			
		Returns:
		
			None
		'''
		
		self.energia = energia
		 
	def coppie(self, sciame, dE, s):
		'''
		Simulo la produzione di coppie elettrone/positrone da parte 
		del fotone.

		Parametri:
		
			sciame(list): Particelle presenti nello sciame
			
			dE(float): Perdita per ionizzazione in una lunghezza di 
			radiazione [Mev]
			
			s(float): Passo della simulazione
			
		Returns:
		
			None: Aggiorna la lista delle particelle presenti, 
			aggiungendo una coppia elettrone positrone 
			con metà dell'energia iniziale
		'''
		
		from Particella import Particella
		nuova_energia = self.energia / 2
		sciame.append(Particella(nuova_energia, dE, s, +1))
		sciame.append(Particella(nuova_energia, dE, s, -1))
		
