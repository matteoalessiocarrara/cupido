# Facebook Filter #

Filtro per profili Facebook, restituisce solo quelli che corrispondono ad una certa
descrizione - libreria in python


## Funzionamento del filtro ##

Le regole del filtro sono definite in un oggetto a parte, derivato da filter_components.FilterRules.
È possibile quindi usare regole personalizzati, e anche cambiare le regole dopo
la creazione del filtro.  

Per utilizzare un filtro, passare l'url di un profilo Facebook al metodo check().
Il filtro dirà se il profilo soddisfa i requisiti richiesti, ed eventualmente 
anche quali requisiti opzionali.


## Scrivere nuovi tipi di filtro ##

Basta scrivere una classe derivata da filter_components.FilterRules, eventualmente
ridefinendo i metodi contenuti e/o i dizionari.


## Requisiti ##
 
 * Gli stessi di [html-facebook-api](https://github.com/matteoalessiocarrara/HTML-Facebook-API)


## Esempio ##

Un software che si basa su questa libreria è [lib-figafind](https://github.com/matteoalessiocarrara/lib-figafind), 
e sto anche scrivendo un interfaccia per questa libreria, aggiungerò il link quando
l'avrò pubblicata.


## Altre informazioni ##

> This is the Unix philosophy: Write programs that do one thing and do it well.
  Write programs to work together. Write programs to handle text streams, because
  that is a universal interface.

Aggiornamenti: [GitHub](https://github.com/matteoalessiocarrara/facebook-filter)  
Email: sw.matteoac@gmail.com
