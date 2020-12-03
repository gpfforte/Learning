# Scrivere ciclo per visualizzaere il codice ascii di ogni carattere di una stringa
S = input('Stringa di cui stampare i codici ASCII?\n')
somma = 0
lista=[]
for x in S:
    asciiValue=ord(x)
    print(asciiValue)
    somma = somma+asciiValue
#    print(map(ord,x))
#    lista.append(map(ord,x))
    lista.append(asciiValue)
print(somma)
print(lista)
#print(map(ord,S))
    