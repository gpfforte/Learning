import pandas as pd
import numpy as np

my_dict1={"x": 4,"y": 5, "b": 7}
my_dict2={"z": 4,"y": 5, "b": 7}
# Conversione di dizionario in serie
my_series1=pd.Series(my_dict1)
my_series2=pd.Series(my_dict2)

print(my_series1["y"])
print(my_series1[1])
print(my_series1)
print(type(my_series1))
# Somma di due serie, fa la somma sulle chiavi corrispondenti elemento per elemento
my_series3=my_series1+my_series2
# Aggiunta di un elemento ad una serie, ho trovato solo append che funzioan tra serie, quindi
# occorre prima trasformare in serie l'elemento da aggiungere
my_series4=my_series1.append(pd.Series({"z": 7}))
print(my_series3)
print(my_series4)
print(my_series4.mean(), np.mean(my_series4))
print(my_series4.std(ddof=True), np.std(my_series4, ddof=True))
print(my_series4.std(ddof=False), np.std(my_series4, ddof=False))
print(my_series4)
# Creazione di un dataframe da una serie
df=pd.DataFrame(my_series4)
# Assegnare nomi alle colonne del dataframe
df.columns=["Numero"]
# Creazione di un'altra colonna
df["Altro Numero"]=my_series4
print("***")
# Assegnazione di un valore ad una cella specifica
df.at["z","Numero"]=23
print(df.loc["z"]["Numero"])
print("***")
print(df.describe())

print(df.index)
print(df)
print(type(df))
print(df.info())
