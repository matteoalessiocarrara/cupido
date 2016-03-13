# FigaFind #

Cerca le ragazze in un gruppo su Facebook


> Esistono ragazze che usano linux? Esistono ragazza che non sono ragazze? Essere o non essere?

Tutte le risposte che cerchi sono qui, in questo incredibile software free!


## Funzionamento ##

Questo piccolo script stampa su stdout un elenco di url, uno per ogni ragazza trovata.


## Come velocizzare la ricerca ##

La ricerca, con le impostazioni predefinite, è abbastanza lenta. Questo però non è un 
problema, è una cosa fatta apposta. Infatti sembra che a Facebook non piacciano i 
bot, quindi questo software cerca di comportarsi come un umano.

Questi sono alcuni trucchi per velocizzare la ricerca, ma considera che Facebook
potrebbe bloccarti il profilo.

 * Utilizza più processi: controllerà più profili contemporaneamente, specifica il
   numero di processi con il parametro --processes
 * Disabilità l'emulazione umana: questa modalità simula i tempi di un essere umano,
   quindi per es. non invierà username e password immediatamente, ma aspetterà un
   po' di tempo facendo finta di scriverli. Questa modalità può essere disattivata
   con il parametro --disable-human-emulation
 * Utilizza di più la cache: recupererà meno spesso alcune informazioni dal server,
   preferendo una copia locale. Questa opzione potrebbe creare dei malfunzionamenti,
   se i dati locali fossero diversi da quelli sul server. Evita quindi di usare il
   profilo mentre questo bot è attivo. Il parametro è --caching-level


## Altre informazioni ##

> This is the Unix philosophy: Write programs that do one thing and do it well. 
  Write programs to work together. Write programs to handle text streams, because 
  that is a universal interface.  

Aggiornamenti: [GitHub](https://github.com/matteoalessiocarrara/FigaFind)  
Email: sw.matteoac@gmail.com
