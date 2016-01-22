# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [3.0.0] - 2015-11-22
### Added
 - htmlfbapi.Facebook.get_email()
 - htmlfbapi.Facebook.get_password()
 - htmlfbapi.Group.get_gid()
 - htmlfbapi.Profile.get_url()
 - htmlfbapi.Profile.get_profile_picture()
 - translations.translate_gender()
 - translations.GENDER_STR_DICT (oggetto GendersDict, con relativi metodi)
 - objects.FBLang: rappresentazione della lingua del profilo, con alcuni metodi
   utili che le stringhe normali non hanno
 - Aggiunti agli oggetti degli attributi property(), in questo modo alcuni metodi
   possono essere chiamati come se fossero attributi
 - Download con più processi in htmlfbapi.Group.get_members()
 - Conversione automatica dell'url in htmlfbapi.Profile.\__init__()
 - Aggiunte librerie multiprocessing, logging, Queue, os
 - Utilizzato il modulo logging
 - Migliorata documentazione
 - Migliorate informazioni per il debug
 - File version.py, aggiunta versione della libreria

### Changed
 - htmlfbap.GENDER_STR_DICT -> translations.GENDER_STR_NDICT
 - htmlfbapi.Requests_Session -> myrequests.Session
 - htmlfbapi.Requests_Session.get2(url) -> myrequests.Session.get2(url, \**kwargs)
 - htmlfbapi.LoginError.\_\_init\_\_() -> myexceptions.LoginError.\__init__(message, res_title, res_text, email, password, \*args):
 - htmlfbapi.Facebook.session() -> htmlfbapi.Facebook.get_session()
 - htmlfbapi.Facebook.user_agent(ua=None, update=False) -> htmlfbapi.Facebook.get_user_agent(),
   htmlfbapi.Facebook.set_user_agent(ua)
 - htmlfbapi.Facebook.lang() -> htmlfbapi.Facebook.get_lang()
 - htmlfbapi.Facebook.gender_str() -> htmlfbapi.Facebook.translate_gender_str()
 - htmlfbapi.Group.members() -> htmlfbapi.Group.get_members()
 - htmlfbapi.Profile.gender() ->  htmlfbapi.Profile.get_gender()
 - Eccezioni spostate nel file myexceptions.py

#### Removed
 - htmlfbapi.HOME_URL
 - htmlfbapi.LOGIN_URL
 - htmlfbapi.HTTPError
 - htmlfbapi.Facebook.LOGIN_OK_TITLE
 - htmlfbapi.Profile.gender_title

#### Fixed
 - myrequests.Session.get2 adesso utilizza i kwargs
 - htmlfbapi.Profile.get_gender() adesso restituisce sempre una stringa,
   anche in caso di sesso non trovato


## [2.1.0] - 2015-10-19
### Added
 - Nuovo metodo per la traduzione del sesso, Facebook.gender_str()
 - Aggiunta opzione per stampare il numero dei profili scaricati in Group.members()
 - Aggiunta traduzione per Profile.gender_title


## [2.0.0] - 2015-9-27
### Removed
 - Eliminate librerie non usate

### Changed
 - Migliorato codice
 - Migliorata documentazione

### Added
 - Nuovi metodi
 - Nuovo oggetto Profile

### Fixed
 - Risolto bug con il metodo Group.members()


## [1.0.0] - 2015-9-24
 - Prima versione
