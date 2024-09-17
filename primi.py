from math import trunc
c = 0
while c != "1" and c != "2":
    c = input("""Vuoi calcolare:
    (1) I numeri primi minori di un certo numero 
    (2) La scomposizione in numeri primi di un certo numero 
    Digita la scelta: """)

if c == "1":
    # Trovo i numeri primi minori di un certo numero preso come input
    ancora = True
    while ancora:
        # Lista che conterrà i numeri primi, contiene già 1 perché quello ci sarà sicuramente
        primi = [1]
        continua = True
        while continua:
            a = input("Inserire Numero Intero da cui partire: ")
            try:
                a_int = int(a)
                continua = False
            except:
                print("Il numero inserito non è un intero")
            a_orig = a_int
        # Verifico se si riesce a scomporre in fattori primi i numeri prima di quello scelto
        # Se si riesce metto i fattori in un dizionario, se il dizionario alla fine è vuoto
        # vuol dire che non era divisibile se non per se stesso e 1, quindi è un numero primo
        # che aggiungo alla lista
        # La funzione range non include l'estremo superiore
        for i in range(2, a_orig+1):
            is_prime = True
            # Per ogni numero guardo se è divisibile per qualche numero da 2 alla sua metà,
            # Oltre la metà non si va perché non sarebbe ovviamente divisibile, e la metà
            # l'avrei già individuato con il 2
            for j in range(2, trunc(i/2+1)):
                # print(i)
                if i % j == 0:
                    is_prime = False
                    break
            if is_prime:
                # Se il dizionario è ancora vuoto il numero che sto indagando è un numero primo
                primi.append(i)
        print(primi)
        d = input("Vuoi provare ancora? (n per terminare) ")
        if d == "n":
            ancora = False
if c == "2":
    # Trvo la scomposizione in numeri primi di un certo numero
    ancora = True
    while ancora:
        scomp = {}
        continua = True
        while continua:
            a = input("Inserire Numero Intero da scomporre: ")
            try:
                a_int = int(a)
                continua = False
            except:
                print("Il numero inserito non è un intero")

        # print (a)
        a_orig = a_int
        for i in range(2, trunc(a_int/2+1)):
            # Per ogni numero guardo se è divisibile per qualche numero da 2 alla sua metà,
            # Oltre la metà non si va perché non sarebbe ovviamente divisibile, e la metà
            # l'avrei già individuato con il 2
            # print(i)
            while a_int % i == 0:
                # print(scomp)
                # Una volta individuato il divisore devo effettivamente dividere per
                # continuare il giro di scomposizione
                a_int = a_int/i
                if i in scomp:
                    # Se è già presente il fattore, aggiungo al suo valore
                    scomp[i] = scomp[i]+1
                else:
                    # Altrimento aggiungo la chiave e come valore di default avrà
                    # ovviamente valore 1 (=esponente)
                    scomp.setdefault(i, 1)
        if not scomp:
            # Se il dizionario è ancora vuoto il numero che sto indagando è un numero primo
            print("Il numero inserito è primo :", a_orig)
        else:
            for k in scomp.keys():
                print("Fattore:", k, "Esponente:", scomp[k])
        b = input("Vuoi provare ancora? (n per terminare) ")
        if b == "n":
            ancora = False
