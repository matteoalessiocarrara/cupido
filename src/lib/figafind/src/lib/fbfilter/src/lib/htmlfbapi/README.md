# HTML Facebook API #

Estensione di facebook-wrapper, livello di astrazione sopra alla rappresentazione
pura del sito - libreria in python


## Miglioramenti rispetto a fbwrapper ##

L'obbiettivo di questa estensione è: assegnare un valore "logico" ai dati, e aggiungere
altre operazioni che di solito vengono fatte dal cervello umano.  

Per esempio, un uomo sa che le stringhe "Donna" e "Female" sono equivalenti, ma
il computer no. Usando solo fbwrapper, un codice come

```python
if profile.gender == "Female":
	...
```

non funzionerebbe se profile.gender fosse "Donna", pur avendo lo stesso significato
logico. Questo non è un problema, fino a quando si scrivono piccoli script da usare
con il proprio profilo, ma è un problema se si pensa di condividere questi script
con altre persone.  

Questa estensione include delle traduzioni per il return di alcuni metodi, quindi
l'esempio precedente potrà essere scritto come:

```python
if profile.gender['English (US)'] == "Female":
	...
```

E funzionerà anche se la stringa recuperata dal server fosse "Donna", perché
prima di confrontarla viene tradotta in 'English (US)'.


## Esempio ##


```python
import logging

import htmlfbapi


logging.basicConfig(level=logging.INFO)


username = raw_input("Username: ")
password = raw_input("Password: ")

# Questo è solo un test veloce, l'human emulation è una rottura di scatole
fb = htmlfbapi.Facebook(username, password, human_emulation_enabled=False)


your_gender = fb.my_profile.gender
your_gender_translations = your_gender.keys()

print "Tu sei:", your_gender
print "Questo genere può essere tradotto in queste lingue:", your_gender_translations


try:
	# Esempio di confronto che funziona indipendentemente dalla lingua del profilo
	# Anche se your_gender è stato recuperato in italiano, francese, o arabo, 
	# questo confronto funziona comunque, perché prima di confrontare traduce
	# nella stessa lingua (English (US))
	if your_gender['English (US)'] == "Female":
		print "Test ok"

except KeyError:
	print "Non c'è una traduzione in inglese per il genere del tuo profilo :/"

```

## Requisiti ##
 
 * Gli stessi di [facebook-wrapper](https://github.com/matteoalessiocarrara/facebook-wrapper)


## Quando posso aggiornare la libreria senza far esplodere il software che la usa? ##

La libreria può essere aggiornata senza problemi finche version.version_major rimane 
uguale.


## Altre informazioni ##

> This is the Unix philosophy: Write programs that do one thing and do it well.
  Write programs to work together. Write programs to handle text streams, because
  that is a universal interface.

Aggiornamenti: [GitHub](https://github.com/matteoalessiocarrara/HTML-Facebook-API)  
Email: sw.matteoac@gmail.com
