# FigaFind #

> Esistono ragazze che usano linux? Esistono ragazza che non sono ragazze? Essere o non essere?

Tutte le risposte che cerchi sono qui, in questo incredibile software free!

## File ##

* main.py: software più bello "graficamente"
* unix_main.py: software più semplice da usare con altri programmi, prende tutte le informazioni da argv e restituisce i profili trovati su stdout
* gid.py: prova ad estrarre il gid da un url

## Sintassi ##

* unix_main.py username password id_gruppo
* gid.py url_gruppo

## Trovare il gid ##

### Manualmente ###

Questo è un esempio di indirizzo:

> https://m.facebook.com/groups/835804479773549?refid=27

Il gid è il numero dopo "/groups/", fino a "?": "835804479773549"

### Con gid.py ###

In ./src/ c'è un piccolo programma (gid.py) che estrae il gid da un url, ma con alcune versioni di facebook potrebbe non funzionare

## Errori ##

* Output non atteso con gid.py: mettere l'url fra ""
* Errore di login con unix_main, anche se la password è giusta: mettere la password fra ""

## Altre informazioni ##

> This is the Unix philosophy: Write programs that do one thing and do it well. Write programs to work together. Write programs to handle text streams, because that is a universal interface.  

Aggiornamenti: [GitHub] (https://github.com/matteoalessiocarrara)  
Email: sw.matteoac@gmail.com