import redis
import subprocess

# Parametri di connessione
redis_host = "redis-11457.c3.eu-west-1-2.ec2.cloud.redislabs.com"
redis_port = 11457
redis_password = "Password"

# Connettiti al server Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

print("\nScegli l'opzione desiderata: ")
print("1. Registrazione")
print("2. Login")
print("3. Cambia stato disturb/no disturb")
print("4. Esci")

scelta = input("Inserisci il numero dell'opzione: ")
print(f"Hai scelto l'opzione {scelta}")

if scelta == '1':
    subprocess.call(["python", "registrazione.py"])
elif scelta == '2':
    subprocess.call(["python", "login.py"])
elif scelta == '3':
    username = input("Inserisci il nome utente: ")

    # Utilizza hget per ottenere il valore corrente dello stato disturb/no disturb
    stato_attuale = redis_client.hget(username, 'Field')
    print(f"Stato attuale per {username}: {stato_attuale}")
    print(f"Hash per {username} prima del cambiamento: {redis_client.hgetall(username)}")

    if stato_attuale is not None:
        nuovo_stato = '1' if stato_attuale == '0' else '0'  # Inverti il valore
        redis_client.hset(username, 'Field', nuovo_stato)  # Imposta il nuovo stato
        print(f"Stato disturb/no disturb cambiato a: {nuovo_stato}")
        print(f"Hash per {username} dopo il cambiamento: {redis_client.hgetall(username)}")
    else:
        print(f"Utente {username} non trovato nel database.")
elif scelta == '4':
    print("Hai scelto di uscire.")
else:
    print("Opzione non valida. Per favore, scegli un'opzione valida.")
