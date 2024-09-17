from numpy.core.shape_base import vstack
from servizio import log_setup
import os
from time import perf_counter
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

start = perf_counter()
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile="DEBUG", name=__name__)
logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")

df = pd.DataFrame()
# print(df.shape)


def main():
    months = [str(x).zfill(2) for x in range(1, 13)]
    m = np.array(months)
    print(m, m.ndim, m.shape, m.dtype, m.size, m.data)
    a = np.arange(30, dtype=np.int64)
    print(a, a.ndim, a.shape, a.dtype, a.size, a.data)
    b = a.reshape(2, 3, 5)
    print(b, b.ndim, b.shape)
    f = np.arange(4, dtype=np.int64)
    ft = f.T
    print(f.dot(ft))
    print(f.shape, ft.shape)
    g = f[np.newaxis, :]
    h = f[:, np.newaxis]
    print("g, g.shape", g, g.shape)
    print("h, h.shape", h, h.shape)
    print("g:", [g < 2])
    print("g:", g[g < 2])
    print("h:", [h < 2])
    print("h:", h[h < 2])
    print(g @ h)
    print(h @ g)
    print(f.dot(f))
    print(f @ f)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if PROVA:
            logger.info(e, exc_info=True)
        else:
            logger.critical(e, exc_info=True)
logger.info("Fine")
end = perf_counter()
print("Elapsed Time: ", end - start)
