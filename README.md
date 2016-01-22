# HTML Facebook API #

API non ufficiali basate sul codice HTML di Facebook

## Cosa è questa libreria ##

Con questa libreria il computer dovrebbe poter fare tutto quello che un uomo
può fare su facebook.

Il funzionamento è semplice: si ha un "browser virtuale" (htmlfbapi.Facebook)
dove è già stato fatto il login su Facebook.  
Il "browser" può essere gestito manualmente, ma per rendere semplice l'utilizzo
della libreria sono stati scritti dei metodi che lo gestiscono automaticamente.
Per esempio, per conoscere la lingua del profilo non è necessario impazzire
con il codice HTML, basta usare il metodo htmlfbapi.Facebook.get_lang() che gestirà
automaticamente il browser per recuperare la lingua.  
Sono anche stati creati degli oggetti che rappresentano oggetti su Facebook:
htmlfbapi.Group per esempio rappresenta un gruppo, mentre htmlfbapi.Profile
rappresenta un profilo. Come gli oggetti rappresentati, anche questi hanno delle
proprietà (attributi) e delle azioni (metodi). Per esempio, un oggetto
htmlfbapi.Group ha una proprietà (attributo) members, che rappresenta la lista
dei partecipanti.  
Purtroppo, questa libreria può essere molto potente ma anche molto instabile:
tutti i metodi si basano su delle "costanti" nel codice HTML, che proprio costanti
non sono, visto che Facebook le può cambiare da un momento all'altro. Anche se,
fortunatamente, questo non succede molto spesso.

## Esempio ##

(Questo esempio, scritto meglio, è anche in src/esempio.py2)

```python
# file della libreria
import htmlfbapi
import version

import sys

if len(sys.argv) != 2 +1:
	print "Uso:", argv[0], "email password"
	exit()

email, password = sys.argv[1:]

print "HTMLFBAPI v.", version.version_str

if version.MAJOR != 3:
	print "Versione della libreria incompatibile!"
	exit()

print "Creiamo un browser virtuale e facciamo il login"
browser = htmlfbapi.Facebook(email, password)

print "Andiamo in un gruppo ora"
# https://m.facebook.com/groups/102915623163953
gruppo = browser.get_group("102915623163953")

print "Il gid del gruppo è %s" % gruppo.gid

print "Scarichiamo la lista dei partecipanti"
print "Usiamo due processi e attiviamo il contatore dei download"
profili = gruppo.get_members(verbose=True, processes=2)

print "Ora stampiamo tutti i nomi che iniziano con \"a\""
for profilo in profili:
	nome = profilo['name'].lower()
	if nome[0] == "a":
		print profilo['name']

print "Scarichiamo un profilo"
profilo = browser.get_profile("/zuck")

print profilo.url, "è", profilo.gender
print "Link alla sua immagine del profilo: %s" % profilo.profile_picture
```

## Librerie richieste ##
 * [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/#Download)

## Oggetti e metodi ##

In doc/MAN.txt c'è la documentazione generata automaticamente da pydoc. Comunque,
in caso di dubbi si può leggere anche il codice, ci sono molti commenti.

## Quando vengono aggiunti nuovi oggetti, metodi e altra roba? ##

Quando mi servono xD
In realtà l'intenzione non era quella di creare una libreria completa, anche se
sarebbe interessante. Ho semplicemente separato questa libreria da altri miei software,
per questo ha solo la roba che serve per far funzionare quei software. Comunque,
dovrebbe essere semplice aggiungere nuovi metodi, che aggiungerò anche io stesso
in futuro.  
Questa libreria verrà comunque aggiornata se Facebook dovesse cambiare il codice
HTML, creando dei bug in alcuni metodi.  
Se avete migliorato questa libreria, se volete potete inviarmi le modifiche, così
gli altri non dovranno perdere tempo a riscrivere quello che avete già scritto.

## Quando posso aggiornare la libreria senza far esplodere il software che la usa? ##
La libreria può essere aggiornata senza problemi finche version.MAJOR rimane uguale.

## Standards ##
* Il codice è scritto per python 2
* Viene usato il modulo logging per gestire i log
* Per il numero di versione si usa [Semantic Versioning](http://semver.org/)
* Nel codice si usano dei tag per i commenti:
  * TODO: cose da fare, prima o poi
  * HACK: soluzione provvisoria ad un problema
  * XXX: fa schifo ai maiali ma funziona, riscrivere
  * FIXME: qualcosa che non funziona

## Modificare la libreria ##

Scrivere nuovi metodi è molto semplice, tutto si basa sul download di pagine da
Facebook e l'estrazione dei dati dal codice HTML. Per il download, si deve usare
l'oggetto requests.Session di htmlfbapi.Facebook: htmlfbapi.Facebook.session.

Per scaricare una pagina con un profilo (oggetto htmlfbapi.Facebook), basta fare

```python
profilo.session.get(url_pagina)
```

dove ovviamente profilo è l'oggetto htmlfbapi.Facebook.

Per degli esempi, leggere il codice in della libreria in /src, è commentato ed è
abbastanza semplice.

## Altre informazioni ##

> This is the Unix philosophy: Write programs that do one thing and do it well.
Write programs to work together. Write programs to handle text streams, because
that is a universal interface.

Aggiornamenti: [GitHub](https://github.com/matteoalessiocarrara)  
Email: sw.matteoac@gmail.com
