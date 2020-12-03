def reverse(x):
    z=[]
    xmax=len(x)
    ll=list(x)
    for y in range (0,xmax):
        z.append(ll[xmax-1-y])
    k="".join(z)
    return (k)
print (reverse('cinzia'))

       