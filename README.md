# Sciame elettromagnetico
La cartella contiene i codici necessari ad implementare e a testare la simulazione di uno sciame elettromagnetico.
Il progetto è diviso in moduli:
  ## Classi
  * Fotone.py
  * Particella.py
  * Sciame.py 

  ## Test del codice  
  * test.py
    
    Contiene il codice per eseguire una simulazione generica. L'utente deve inserire i seguenti input:
    
      * Energia primaria 
      * Segno della prima particella (+1,0,-1)
      * Passo della simulazione 
      * Perdita per ionizzazione 
      * Energia critica per un elettrone 
      * Energia critica per un positrone 
      * Numero di sciami da simulare 
      * Lunghezza di radiazione 
        
    Il codice produce due grafici, sul numero di particelle e sull'energia depositata in funzione della distanza percorsa dallo sciame

  ## Studio dei vari materiali  
  * Analisi_materiali.py
    
    Contiene il codice per eseguire una simulazione in alcuni materiali. Quelli utilizzati sono ghiaccio e cemento ma altri possono essere facilmente aggiunti.
    L'utente deve inserire i seguenti input:
    
      * Numero di campioni di energia 
      * Ordine di grandezza dell'energia massima
      * Moltiplicatore energia massima 
      * Passo della simulazione 
      * Numero di ripetizioni statistiche 
      * Segno della particella iniziale 
        
    Il codice produce due grafici, sulla distanza percorsa e sull'energia depositata in funzione dell'energia primaria.


