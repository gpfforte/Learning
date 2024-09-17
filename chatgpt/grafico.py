import numpy as np
import matplotlib.pyplot as plt

# Definisci la funzione polinomiale


def f(x):
    return x**2

# Definisci la derivata della funzione polinomiale


def df(x):
    return 2*x


# Crea un array di valori di x
x = np.linspace(-10, 10, 1000)

# Calcola i valori di y per la funzione polinomiale e per la sua derivata
y = f(x)
dy = df(x)

# Crea il grafico della funzione polinomiale
plt.plot(x, y, label="f(x) = x^2")

# Crea il grafico della derivata della funzione polinomiale
plt.plot(x, dy, label="f'(x) = 2x")

# Aggiungi la legenda al grafico
plt.legend()

# Mostra il grafico
plt.show()
