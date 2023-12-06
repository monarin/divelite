from dask.distributed import Client, progress
client = Client(threads_per_worker=4, n_workers=1)

import time
import random

def costly_simulation(list_param):
    time.sleep(random.random())
    return sum(list_param)

if __name__ == "__main__":
    t0 = time.monotonic()
    costly_simulation([1,2,3,4])
    t1 = time.monotonic()
    print(f'serial {t1-t0:.5f}s.')
