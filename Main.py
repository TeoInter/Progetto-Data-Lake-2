import Funzioni

print("\nScegli l'opzione desiderata: ")
print("1. Registrazione")
print("2. Login")
print("3. Esci")

scelta = input("Inserisci il numero dell'opzione: ")
print(f"Hai scelto l'opzione {scelta}")

if scelta == '1':
    Funzioni.registrare_utente()
elif scelta == '2':
    nome_utente = Funzioni.login()
    if nome_utente is not None:
        print("Accesso eseguito, cosa vuoi fare?\n1)Attiva/disattiva Dnd\n2)Visualizza Lista Amici\n3)Ricerca Utente")
        selezione = input("Fai la tua scelta: ")
        if int(selezione) == 1:
            Funzioni.visualizza_stato(nome_utente)
        if int(selezione) == 2:
            lista_amici = Funzioni.ottenere_lista_amici(nome_utente)
            print(lista_amici)
        if int(selezione) == 3:
            utente_cercato = Funzioni.cercare_utenti()
            print(f"Desideri aggiungere {utente_cercato} agli amici (y/n)? ")
            if input() == 'y':
                Funzioni.aggiungere_amico(nome_utente=nome_utente, nome_amico=utente_cercato)
        else:
            print("Errore, selezione non valida")
elif scelta == '3':
    print("Hai scelto di uscire.")
else:
    print("Opzione non valida. Per favore, scegli un'opzione valida.")

