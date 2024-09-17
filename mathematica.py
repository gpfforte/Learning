import math
import os

import numpy as np
from matplotlib import pyplot as plt

# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
plt.style.use("seaborn")

fig1, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(6, 6))

xx = list(np.linspace(0, 3 * np.pi, num=100))
yy = [math.sin(n) for n in xx]
zz = [math.cos(n) for n in xx]
tt = [math.tan(n) for n in xx]
ax1.plot(xx, yy)
ax1.set_title("sin")
ax2.plot(xx, zz)
ax2.set_title("cos")
ax3.plot(xx, tt)
ax3.set_title("tan")
fig1.tight_layout()
plt.axis()


x = np.linspace(0, 10, 11)
y = [3.9, 4.4, 10.8, 10.3, 11.2, 13.1, 14.1, 9.9, 13.9, 15.1, 12.5]


# fit a linear curve an estimate its y-values and their error.
a, b = np.polyfit(x, y, deg=1)
y_est = a * x + b
y_err = x.std() * np.sqrt(
    1 / len(x) + (x - x.mean()) ** 2 / np.sum((x - x.mean()) ** 2)
)

fig2, ax = plt.subplots()
ax.plot(x, y_est, "-")
ax.fill_between(x, y_est - y_err, y_est + y_err, alpha=0.2)
ax.plot(x, y, "o", color="tab:red")
plt.show()

