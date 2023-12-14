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
    # Implementa la logica di registrazione qui

def login():
    print("Hai scelto l'opzione di login.")
    # Implementa la logica di login qui

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

# Menu principale
while True:
    print("\nScegli un'opzione:")
    print("1. Registrazione")
    print("2. Login")
    print("3. Cambia stato disturb/no disturb")
    print("4. Esci")

    scelta = input("Inserisci il numero dell'opzione: ")

    if scelta == '1':
        registrazione()
    elif scelta == '2':
        login()
    elif scelta == '3':
        username = input("Inserisci il nome utente: ")
        cambia_stato(username)
    elif scelta == '4':
        print("Hai scelto di uscire.")
        break
    else:
        print("Opzione non valida. Per favore, scegli un'opzione valida.")
