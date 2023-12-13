import redis

redis_host = "redis-11457.c3.eu-west-1-2.ec2.cloud.redislabs.com"
redis_port = 11457
redis_password = "Password"

redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

def controllare_disponibilita_nome_utente(nome_utente):
    return not redis_client.hexists("prova", nome_utente)

def registrare_utente(nome_utente, password,dnd):
    if not controllare_disponibilita_nome_utente(nome_utente):
        return f"Il nome utente '{nome_utente}' è già in uso. Scegli un altro nome."
    redis_client.hset("prova", nome_utente,password)
    redis_client.hset("stato", nome_utente, dnd)
    return f"Registrazione avvenuta con successo per {nome_utente}"



nome_utente = input("Inserisci il nome utente: ")
password = input("Inserisci la password: ")
dnd = 0 #valore di Default, vuol dire non attivo

risultato_registrazione = registrare_utente(nome_utente, password,dnd)
print(risultato_registrazione)
