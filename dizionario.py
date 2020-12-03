d={'c':1,'b':2,'a':3,'d':4,'e':5,'f':6}

keys=d.keys()
#keys.sort()
#for key in keys:
#    print (key,'=>',d[key])

for key in sorted(d):
    print (key,'=>',d[key])

