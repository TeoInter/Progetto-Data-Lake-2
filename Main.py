import redis

# Parametri di connessione
redis_host = "redis-11457.c3.eu-west-1-2.ec2.cloud.redislabs.com"
redis_port = 11457
redis_password = "Password"

# Connettiti al server Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Dati di prova
nome_utente = "Alice"
password = "mypass123"
altro_dato = "Qualsiasi altro dato"

# Esegui l'inserimento
redis_client.hset("utenti", nome_utente, password)
redis_client.hmset(nome_utente, {'altro_dato': altro_dato})

print(f"Dati di prova inseriti con successo per {nome_utente}")
