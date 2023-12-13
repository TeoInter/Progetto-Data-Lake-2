from connessione import connessione
redis_client = connessione()

def ottenere_password(nome_utente):
    if not redis_client.hexists("utenti", nome_utente):
        return "Utente non trovato."
    password = redis_client.hget("utenti", nome_utente)
    return password

def login():
    nome_utente = input("Inserisci il nome utente: ")
    password_giusta = ottenere_password(nome_utente)
    password_digitata = input("Inserisci password: ")
    if password_digitata == password_giusta:
        print(f"Accesso, ciao {nome_utente}")
    else:
        print("Password e/o username non validi")

if __name__ == '__main__':
    login()