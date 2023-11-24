import os
from multiprocessing import Pool
import time
import math

N = 10

def run_npm_start():
    print("HOLA SERVER")
    os.system('npm start')
    print("ADIOS SERVER")

def run_python_client_recv(n):
    print("HOLA RECEIVER")
    os.system(f"python client_recv.py {n}")
    print("ADIOS RECEIVER")

def run_python_client_send(n):
    print("HOLA SENDER")
    os.system(f"python client_send.py {n}")
    print("ADIOS SENDER")

def ranging(N: int, n_samples: int):
    ratio = (float(N)) ** (1.0 / (n_samples - 1))
    samples = [1]
    for i in range(1, n_samples):
        samples.append(samples[-1] * ratio)
    integer_samples = set([round(sample) for sample in samples])
    integer_samples = list(integer_samples)
    integer_samples.sort()
    return integer_samples


if __name__ == "__main__":
    with Pool() as pool:
        for n in range(1, N):
            pool.apply_async(run_npm_start)
            time.sleep(5)
            pool.apply_async(run_python_client_recv, args=(n,))
            time.sleep(2)
            pool.apply_async(run_python_client_send, args=(n,))
            time.sleep(20)
