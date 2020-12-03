numero = input('Di che numero vuoi calcolare il fattoriale?\n')
intero = int(numero)
fattoriale = 1
for n in range (1,intero+1):
    print (n)
    fattoriale = fattoriale*n
print('Il fattoriale di %d è %d' %(intero,fattoriale))    
