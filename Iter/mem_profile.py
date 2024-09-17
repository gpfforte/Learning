from multiprocessing.dummy import Process
from pympler import summary, muppy
import psutil
import os
import sys


def memory_usage_psutil():
    # return the memory usage in MB
    process = psutil.Process(os.getpid())
    print(type(process.memory_info()))
    print(process.memory_info())
    print(process.memory_info()[0])
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem


print(memory_usage_psutil())
