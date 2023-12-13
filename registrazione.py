from connessione import connessione


redis_client = connessione()

def controllare_disponibilita_nome_utente(nome_utente):
    return not redis_client.hexists("utenti", nome_utente)

def registrare_utente(nome_utente, password,dnd):
    if not controllare_disponibilita_nome_utente(nome_utente):
        return f"Il nome utente '{nome_utente}' è già in uso. Scegli un altro nome."
    redis_client.hset("utenti", nome_utente,password)
    redis_client.hset("stato", nome_utente, dnd)
    return f"Registrazione avvenuta con successo per {nome_utente}"



nome_utente = input("Inserisci il nome utente: ")
password = input("Inserisci la password: ")
dnd = 0 #valore di Default, vuol dire non attivo

risultato_registrazione = registrare_utente(nome_utente, password,dnd)
print(risultato_registrazione)
