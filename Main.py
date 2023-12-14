import redis
import subprocess

# Parametri di connessione
redis_host = "redis-11457.c3.eu-west-1-2.ec2.cloud.redislabs.com"
redis_port = 11457
redis_password = "Password"

# Connettiti al server Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

def registrazione():
    print("Hai scelto l'opzione di registrazione.")
    # Esegui il modulo registrazione.py come processo separato
    subprocess.call(["python", "registrazione.py"])

def login():
    print("Hai scelto l'opzione di login.")
    # Esegui il modulo login.py come processo separato
    subprocess.call(["python", "login.py"])

def cambia_stato(username):
    # Verifica se l'utente esiste nel database
    if redis_client.hexists("stato", username):
        # Ottieni il valore corrente
        stato_attuale = redis_client.hget("stato", username)

        # Inverti il valore corrente
        nuovo_stato = '1' if stato_attuale == '0' else '0'

        # Imposta il nuovo valore nel campo 'Field'
        redis_client.hset("stato", username, nuovo_stato)

        print(f"Stato disturb/no disturb per {username} cambiato a: {nuovo_stato}")
    else:
        print(f"L'utente {username} non esiste nel database.")

def invia_messaggio(destinatario, mittente, messaggio):
    # Verifica se il destinatario è un amico dell'utente mittente
    if redis_client.sismember(f"amici:{mittente}", destinatario):
        # Ottieni lo stato corrente del destinatario
        stato_destinatario = redis_client.hget("stato", destinatario)

        # Verifica se il destinatario è in modalità "Do Not Disturb"
        if stato_destinatario == '1':
            print(f"Errore: Impossibile inviare il messaggio a {destinatario}. Il destinatario è in modalità 'Do Not Disturb'.")
        else:
            # Aggiungi il messaggio alla coda del destinatario
            coda_destinatario = f"coda:{destinatario}"
            messaggio_da_inviare = f"{mittente}: {messaggio}"
            redis_client.rpush(coda_destinatario, messaggio_da_inviare)
            print(f"Messaggio inviato a {destinatario}: {messaggio}")
    else:
        print(f"Errore: {destinatario} non è nella lista amici di {mittente}.")

def leggi_messaggi(username):
    # Recupera i messaggi dalla coda dell'utente
    coda_utente = f"coda:{username}"
    messaggi = redis_client.lrange(coda_utente, 0, -1)

    if messaggi:
        print(f"\nMessaggi per {username}:")
        for messaggio in messaggi:
            print(messaggio)
    else:
        print(f"Nessun messaggio per {username}.")

# Menu principale
while True:
    print("\nScegli un'opzione:")
    print("1. Registrazione")
    print("2. Login")
    print("3. Cambia stato disturb/no disturb")
    print("4. Invia messaggio")
    print("5. Leggi messaggi")
    print("6. Esci")

    scelta = input("Inserisci il numero dell'opzione: ")

    if scelta == '1':
        registrazione()
    elif scelta == '2':
        login()
    elif scelta == '3':
        username = input("Inserisci il nome utente: ")
        cambia_stato(username)
    elif scelta == '4':
        mittente = input("Inserisci il tuo nome utente: ")
        destinatario = input("Inserisci il destinatario del messaggio: ")
        messaggio = input("Inserisci il messaggio: ")
        invia_messaggio(destinatario, mittente, messaggio)
    elif scelta == '5':
        username = input("Inserisci il nome utente: ")
        leggi_messaggi(username)
    elif scelta == '6':
        print("Hai scelto di uscire.")
        break
    else:
        print("Opzione non valida. Per favore, scegli un'opzione valida.")
