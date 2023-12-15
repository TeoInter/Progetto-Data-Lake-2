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
    while True:
        if nome_utente is not None:
            print("Cosa vuoi fare?\n\n1) Attiva/disattiva Dnd\n2) Visualizza Lista Amici\n3) Ricerca Utente\n4) Scrivi Messaggio\n5) Esci\n")
            selezione = input("Fai la tua scelta: ")
            if int(selezione) == 1:
                Funzioni.stato(nome_utente)
            elif int(selezione) == 2:
                lista_amici = Funzioni.ottenere_lista_amici(nome_utente)
                print(lista_amici)
            elif int(selezione) == 3:
                utente_cercato = Funzioni.cercare_utenti()
                print(f"Desideri aggiungere {utente_cercato} agli amici (y/n)? ")
                if input() == 'y':
                    Funzioni.aggiungere_amico(nome_utente=nome_utente, nome_amico=utente_cercato)
            elif int(selezione) == 4:
                lista_amici = list(Funzioni.ottenere_lista_amici(nome_utente))
                destinatario = Funzioni.scegli_amico_da_lista(lista_amici)
                Funzioni.invia_messaggio(mittente=nome_utente, destinatario=destinatario)
            elif selezione == '5':
                print("Hai scelto di uscire.")
                break
            else:
                print("Errore, selezione non valida")
elif scelta == '3':
    print("Hai scelto di uscire.")
else:
    print("Opzione non valida. Per favore, scegli un'opzione valida.")

