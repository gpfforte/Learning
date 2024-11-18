
from matplotlib import pyplot as plt

import os
import numpy as np
import math
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# plt.style.use("fivethirtyeight")
# plt.style.use("dark_background")
plt.style.use("classic")
# plt.xkcd()
l=np.linspace(0,1,1000) # lunghezza pendolo in metri
# print(l)
G=9.81 # Costante gravitazionale in metri/secondi quadri
# La parte qui sotto è equivalente alla riga asteriscata ancora più sotto, ma con np.sqrt() è decisamene più semplice
# def period(l):
#     return 2*math.pi*math.sqrt(l/G)

# vperiod=np.vectorize(period)
# t = vperiod(l)
t=2*math.pi*np.sqrt(l/G)

plt.plot(l, t, label='Period')
plt.xlabel('Lenght [m]')
plt.ylabel('Period [s]')
plt.title('Pendulum period variation over pendulum lenght')
plt.legend()
plt.tight_layout()
plt.savefig('Images/pendulum.png')
plt.grid()
plt.show()