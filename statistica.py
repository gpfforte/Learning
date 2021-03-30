import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd
x = [8.0, 1, 2.5, 4, 28.0]
x_with_nan = [8.0, 1, 2.5, math.nan, 4, 28.0]
y, y_with_nan = np.array(x), np.array(x_with_nan)
z, z_with_nan = pd.Series(x), pd.Series(x_with_nan)
mean_ = statistics.fmean(x)
print(mean_)
mean_ = statistics.fmean(x_with_nan)
print(mean_)
mean_=np.nanmean(y_with_nan)
print(mean_)
mean_=z.mean()
print(mean_)
mean_=z_with_nan.mean()
print(mean_)
w = [0.1, 0.2, 0.3, 0.25, 0.15]
wmean = sum(w[i] * x[i] for i in range(len(x))) / sum(w)
print(wmean)