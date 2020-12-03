L=[1,2,4,8,16,32,64]
X=5
found=i=0
while not found and i<len(L):
    if 2**X==L[i]:
        found=1
    else:
        i=i+1
    if found:
        print('at index',i)
else:
    if not found:
        print (X,'not found')
            
Y=2**X
if Y in L:
    print ("Trovato all'indice",L.index(Y))
else:
    print('Non trovato')