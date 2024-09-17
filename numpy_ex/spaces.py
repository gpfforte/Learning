from logging import DEBUG
from servizio import log_setup
import os
from time import perf_counter
import numpy as np

start = perf_counter()
# Setta la working directory al path dello script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setta il log
filename, _ = os.path.splitext(os.path.basename(__file__))
logger = log_setup.logging_setup(
    nomefile=filename, levelfile=DEBUG, name=__name__)
logger.info("Inizio")

PROVA = bool(os.environ.get("AMBIENTE_DI_PROVA") == "SI")


# 50 values between 1 and 10:
def esempi():
    m = np.linspace(1, 10)
    print(m, m.ndim, m.shape, m.dtype, m.size, m.data)

    # 7 values between 1 and 10:
    m = np.linspace(1, 10, 7, endpoint=True)
    print(m, m.ndim, m.shape, m.dtype, m.size, m.data)

    # 7 values between 1 and 10:
    m = np.linspace(1, 10, 7, endpoint=False)
    print(m, m.ndim, m.shape, m.dtype, m.size, m.data)

    m, n = np.linspace(1, 10, retstep=True)
    print(m, m.ndim, m.shape, m.dtype, m.size, m.data)
    print(n)

    m = np.array(42)
    print(m, m.ndim, m.shape, m.dtype, m.size, m.data)

    m = np.identity(4, dtype=int)
    print(m, m.ndim, m.shape, m.dtype, m.size, m.data)

    m = np.eye(5, 8, k=2, dtype=int)
    print(m, m.ndim, m.shape, m.dtype, m.size, m.data)
    v = np.linspace(0, 10, 10, endpoint=False)
    odd = v[1::2]
    rev = v[::-1]
    print(v)
    print(odd)
    print(rev)
    a = np.array([1, 2, 3, 4, 5])
    b = a[1:4]
    b[0] = 200
    print(a[1])
    m = np.array(
        [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [4, 5, 6, 7, 8],
            [8, 9, 10, 11, 12],
            [13, 14, 15, 16, 17],
        ]
    )
    revm = m[::, ::-1]
    print(revm)
    revmrow = m[::-1, :]
    print(revmrow)
    revmall = m[::-1, ::-1]
    print(revmall)
    cut = m[1:-1, 1:-1]
    print(cut)
    dt = np.dtype(
        [
            ("country", np.unicode, 20),
            ("density", "i4"),
            ("area", "i4"),
            ("population", "i4"),
        ]
    )
    population_table = np.array(
        [
            ("Netherlands", 393, 41526, 16928800),
            ("Belgium", 337, 30510, 11007020),
            ("United Kingdom", 256, 243610, 62262000),
            ("Germany", 233, 357021, 81799600),
            ("Liechtenstein", 205, 160, 32842),
            ("Italy", 192, 301230, 59715625),
            ("Switzerland", 177, 41290, 7301994),
            ("Luxembourg", 173, 2586, 512000),
            ("France", 111, 547030, 63601002),
            ("Austria", 97, 83858, 8169929),
            ("Greece", 81, 131940, 11606813),
            ("Ireland", 65, 70280, 4581269),
            ("Sweden", 20, 449964, 9515744),
            ("Finland", 16, 338424, 5410233),
            ("Norway", 13, 385252, 5033675),
        ],
        dtype=dt,
    )
    print(population_table)
    print(population_table["density"])
    print(population_table["country"])
    print(population_table["area"][2:5])
    print(population_table[:4])
    np.savetxt(
        "population_table.csv", population_table, fmt="%s;%d;%d;%d", delimiter=";"
    )
    x = np.genfromtxt("population_table.csv", dtype=dt, delimiter=";")
    print(x)
    x = np.loadtxt(
        "population_table.csv",
        dtype=dt,
        converters={0: lambda x: x.decode("utf-8")},
        delimiter=";",
    )
    print(x)
    dprod = np.dtype([("product_id", np.int32), ("price", np.float64)])
    product_table = np.array(
        [
            (1, 7.3),
            (2, 4.7),
            (3, 7),
            (4, 2.3),
        ],
        dtype=dprod,
    )
    print(product_table["product_id"])
    print(product_table[0])
    print(product_table["price"][2] == product_table[2]["price"])


def main():
    dtime = np.dtype(
        [("hour", np.int8), ("minute", np.int8), ("second", np.int8)])
    time1 = np.array([(1, 1, 1)], dtype=dtime)
    print(time1)
    pass


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
