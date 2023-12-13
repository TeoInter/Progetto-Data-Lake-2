import redis

redis_host = "redis-11457.c3.eu-west-1-2.ec2.cloud.redislabs.com"
redis_port = 11457
redis_password = "Password"

redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

def controllare_disponibilita_nome_utente(nome_utente):
    return not redis_client.hexists("utenti", nome_utente)

def registrare_utente(nome_utente, password):
    if not controllare_disponibilita_nome_utente(nome_utente):
        return f"Il nome utente '{nome_utente}' è già in uso. Scegli un altro nome."
    redis_client.hset("utenti", nome_utente, password)
    return f"Registrazione avvenuta con successo per {nome_utente}"


nome_utente = input("Inserisci il nome utente: ")
password = input("Inserisci la password: ")

risultato_registrazione = registrare_utente(nome_utente, password)
print(risultato_registrazione)