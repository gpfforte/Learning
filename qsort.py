lista=[41, 7, 41, 23, 23, 42, 23, 42]

def qsort (ll):
    if len (ll) <=1:
        return ll
    else:
        pivot = ll[0]
        sx=[]
        dx=[]
        mm=[]
        for n in range (1,len(ll)):         
            if ll[n] < pivot:
                sx.append(ll[n])
            elif ll[n] > pivot:
                dx.append(ll[n])
            elif ll[n] in ll[:n]: #devo controllare se è presente nella parte di lista già fatta
                mm=mm+[pivot]     #se è presente più di una volta devo tenerne conto sommando le varie volte
        return qsort(sx)+[pivot]+mm+qsort(dx)
print (lista)
print (qsort(lista))

 
                
        