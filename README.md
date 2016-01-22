# HTML Facebook API #

API non ufficiali basate sul codice HTML di Facebook

## Cosa è questa libreria ##

Con questa libreria il computer dovrebbe poter fare tutto ciò che un uomo può fare su facebook.  
Semplificando, il funzionamento è questo: dopo aver fatto il login, si possono scaricare pagine da Facebook ed estrarre i dati, oppure si possono inviare dati. In pratica funziona come un browser, ma qui è controllato dal computer e non dall'utente.  
Purtroppo, questa libreria può essere molto potente (si può fare veramente di tutto!) ma anche molto instabile: si basa tutto su delle "costanti" nel codice HTML, che proprio costanti non sono, visto che Facebook lo può cambiare da un giorno all'altro.

## Esempio ##

Stampa il nome di tutti i membri di un gruppo

```python
import htmlfbapi

email = ""
passw = ""
# id del gruppo, una cosa simile a 1484239995227666 (si trova nell'url di un gruppo)
gid = ""

# connessione a fb
profilo1 = htmlfbapi.Facebook(email, passw)

# il gruppo con id "gid" visto da profilo1
gruppo = profilo1.get_group(gid) 

# scarica i membri
profili = gruppo.members()

# stampa il nome di ogni profilo
for profilo in profili:
	print profilo['name'].encode("utf8")
```

## Modificare la libreria ##

Scrivere nuovi oggetti, metodi o funzioni è veramente molto semplice: si ha un oggetto requests.Session() con il profilo loggato, e i relativi metodi, per es. get() e post().

Per scaricare una pagina con un profilo, basta fare

```python
profilo1.session().get(pagina)
```

avendo ovviamente profilo1 come nell'esempio sopra:

```python
# connessione a fb
profilo1 = htmlfbapi.Facebook(email, passw)
```

Per degli esempi, leggere il codice in ./src, è commentato e abbastanza semplice.

## Oggetti e metodi ##

Leggere il file in ./doc

## Aggiornamenti ##

Questa libreria attualmente è "incompleta", nel senso che non fa molte cose, perché la aggiorno solo quando mi servono nuovi metodi, oggetti ecc. o quando facebook cambia il codice HTML del sito.
Essendo però software free, potete creare la vostra versione, o inviarmi le vostre modifiche, così tutti avranno una libreria migliore.

## Altre informazioni ##

> This is the Unix philosophy: Write programs that do one thing and do it well. Write programs to work together. Write programs to handle text streams, because that is a universal interface.  

Aggiornamenti: [GitHub] (https://github.com/matteoalessiocarrara)  
Email: sw.matteoac@gmail.com
