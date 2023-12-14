import redis

def connessione():
    redis_host = "redis-11457.c3.eu-west-1-2.ec2.cloud.redislabs.com"
    redis_port = 11457
    redis_password = "Password"
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    return redis_client

def login():
    nome_utente = input("Inserisci il nome utente: ")
    password_giusta = ottenere_password(nome_utente)
    password_digitata = input("Inserisci password: ")
    if password_digitata == password_giusta:
        print(f"Accesso, ciao {nome_utente}")
        return nome_utente
    else:
        return None

def ottenere_password(nome_utente):
    if not redis_client.hexists("utenti", nome_utente):
        return "Utente non trovato."
    password = redis_client.hget("utenti", nome_utente)
    return password

def controllare_disponibilita_nome_utente(nome_utente):
    return not redis_client.hexists("utenti", nome_utente)

def registrare_utente():
    nome_utente = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")
    dnd = 0  # valore di Default, vuol dire non attivo
    if not controllare_disponibilita_nome_utente(nome_utente):
        return f"Il nome utente '{nome_utente}' è già in uso. Scegli un altro nome."
    redis_client.hset("utenti", nome_utente,password)
    redis_client.hset("stato", nome_utente, dnd)
    return f"Registrazione avvenuta con successo per {nome_utente}"

def ottenere_lista_amici(nome_utente):
    if not controllare_esistenza_utente(nome_utente):
        return "Utente non trovato."
    lista_amici = redis_client.smembers(f"amici:{nome_utente}")
    return lista_amici

def controllare_esistenza_utente(nome_utente):
    return redis_client.hexists("utenti", nome_utente)

def aggiungere_amico(nome_utente, nome_amico):
    if not controllare_esistenza_utente(nome_utente) or not controllare_esistenza_utente(nome_amico):
        return "Utente o amico non trovato."
    if redis_client.sadd(f"amici:{nome_utente}", nome_amico):
        redis_client.sadd(f"amici:{nome_amico}", nome_utente)
        return f"{nome_amico} aggiunto alla lista degli amici di {nome_utente} (amicizia reciproca)."
    else:
        return f"{nome_amico} è già presente nella lista degli amici di {nome_utente}."

def cercare_utenti():
    nome_cercato = input("Chi vuoi cercare?")
    tutti_utenti = redis_client.hkeys("utenti")
    utente_risultato = [utente for utente in tutti_utenti if nome_cercato.lower() in utente.lower()]
    return utente_risultato

def cambia_stato(nome_utente,valore):
    if int(valore) == 0:
        print("Ci sono")
        valore = 1
    else:
        valore = 0
    redis_client.hset("stato", nome_utente, valore)
    nuovo_valore = redis_client.hget("stato", nome_utente)
    print(f"Nuovo valore per {nome_utente}: {nuovo_valore}")

def visualizza_stato(nome_utente):
    valore = redis_client.hget("stato", nome_utente)
    if valore is not None:
        print(f"Lo stato di {nome_utente} è: {valore}")
        stato = input("Cambiare stato? (y/n)")
        if stato.lower() == 'y':
            cambia_stato(nome_utente,valore)
    else:
        print(f"Il campo {nome_utente} non esiste nel database.")

redis_client = connessione()

