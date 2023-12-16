import redis
import datetime

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
        print(f"{nome_amico} aggiunto alla lista dei tuoi amici.")
    else:
        print(f"{nome_amico} è già tuo amico.")

def cercare_utenti():
    nome_cercato = input("Chi vuoi cercare? ")
    tutti_utenti = redis_client.hkeys("utenti")
    risultato_ricerca = [utente for utente in tutti_utenti if nome_cercato.lower() in utente.lower()]
    if not risultato_ricerca:
        print("Nessun risultato trovato.")
        return None
    elif len(risultato_ricerca) == 1:
        print(f"È stato trovato un solo utente: {risultato_ricerca}")
        return risultato_ricerca[0]
    else:
        print("Sono stati trovati più risultati:")
        for i, utente in enumerate(risultato_ricerca, 1):
            print(f"{i}. {utente}")
        while True:
            scelta = input("Inserisci il numero dell'utente desiderato: ")
            if scelta.isdigit() and 1 <= int(scelta) <= len(risultato_ricerca):
                return risultato_ricerca[int(scelta) - 1]
            else:
                print("Scelta non valida. Riprova.")

def cambia_stato(nome_utente,valore):
    if int(valore) == 0:
        valore = 1
    else:
        valore = 0
    redis_client.hset("stato", nome_utente, valore)
    nuovo_valore = redis_client.hget("stato", nome_utente)
    print(f"{visualizza_stato(nuovo_valore)}ta")

def ottieni_stato(utente):
    valore = redis_client.hget("stato", utente)
    return valore

def visualizza_stato(valore):
    if int(valore)== 1:
        return 'Modalità DnD attiva'
    else:
        return 'Modalita Dnd disattiva'

def stato(nome_utente):
    valore = redis_client.hget("stato", nome_utente)
    if valore is not None:
        print(visualizza_stato(valore))
        stato = input("Cambiare stato? (y/n)")
        if stato.lower() == 'y':
            cambia_stato(nome_utente,valore)
    else:
        print(f"Il campo {nome_utente} non esiste nel database.")

def visualizza_cronologia(mittente, destinatario):
    chiave_cronologia_mittente = f"chat:{mittente}:{destinatario}"
    cronologia_mittente = redis_client.lrange(chiave_cronologia_mittente, 0, -1)
    for messaggio in cronologia_mittente:
        print(messaggio)

def scegli_amico_da_lista(lista_amici):
    while True:
        print("Lista degli amici:")
        for i, amico in enumerate(lista_amici, 1):
            print(f"{i}. {amico}")
        scelta = input("Scegli un amico (inserisci il numero corrispondente): ")
        try:
            indice_scelto = int(scelta)
            if 1 <= indice_scelto <= len(lista_amici):
                amico_scelto = lista_amici[indice_scelto - 1]
                return amico_scelto
            else:
                print("Inserisci un numero valido.")
        except ValueError:
            print("Inserisci un numero valido.")

def invia_messaggio(mittente, destinatario):
    visualizza_cronologia(mittente, destinatario)
    testo = input("Digita il tuo messaggio: ")
    stato_destinatario = ottieni_stato(destinatario)
    if int(stato_destinatario)== 0:
        data_ora_invio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messaggio = f"> {testo} [{data_ora_invio}]"
        chiave_cronologia_mittente = f"chat:{mittente}:{destinatario}"
        redis_client.rpush(chiave_cronologia_mittente, messaggio)
        messaggio = f"< {testo} [{data_ora_invio}]"
        chiave_cronologia_destinatario = f"chat:{destinatario}:{mittente}"
        redis_client.rpush(chiave_cronologia_destinatario, messaggio)
        print("Messaggio inviato correttamente")
    else:
        print(f"L'utente {destinatario} è in modalità non disturbare, riprova più tardi")
redis_client = connessione()