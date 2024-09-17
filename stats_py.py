import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd
x = [8.0, 1, 2.5, 4, 28.0]
x_with_nan = [8.0, 1, 2.5, math.nan, 4, 28.0]
y, y_with_nan = np.array(x), np.array(x_with_nan)
z, z_with_nan = pd.Series(x), pd.Series(x_with_nan)
print(x)
print(y)
print(z)

print(x_with_nan)
print(y_with_nan)
print(z_with_nan)
print(y_with_nan)
