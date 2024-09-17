# Import the required libraries
import numpy as np
import matplotlib.pyplot as plt

xx = np.linspace(-10, 10, 101)
# yy = np.sqrt(xx)
yy = xx**2-5*xx-7

print(xx)
print(yy)

plt.plot(xx, yy)
plt.show()
