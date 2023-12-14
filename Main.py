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
        print("Accesso eseguito, cosa vuoi fare?\n1)Attiva/disattiva Dnd\n2)Visualizza Lista Amici")
        selezione = input("Fai la tua scelta: ")
        if int(selezione) == 1:
            Funzioni.visualizza_stato(nome_utente)
        if int(selezione) == 2:
            print(Funzioni.ottenere_lista_amici(nome_utente))
        else:
            print("Errore, selezione non valida")
elif scelta == '3':
    print("Hai scelto di uscire.")
else:
    print("Opzione non valida. Per favore, scegli un'opzione valida.")

