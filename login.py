import redis

redis_host = "redis-11457.c3.eu-west-1-2.ec2.cloud.redislabs.com"
redis_port = 11457
redis_password = "Password"

# Connettiti al server Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)


def login():
    username = input("Inserisci il nome utente: ")
    password = getpass.getpass("Inserisci la password: ")

    # Verifica le credenziali
    password_memorizzata = redis_client.hget("utenti", username)
    if password == password_memorizzata:
        print("Accesso effettuato con successo!")
    else:
        print("Nome utente o password non validi.")


login()
