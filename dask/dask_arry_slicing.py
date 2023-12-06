import dask.array as da
import numpy as np
import random
import time

n_samples = 10000000
ts = random.sample(range(n_samples), n_samples)
t0 = time.monotonic()
da_ts = da.from_array(ts, chunks='auto')
t1 = time.monotonic()
print(f'Created {da_ts} in {t1-t0:.2f}s.')
inds = da_ts.argtopk(-da_ts.shape[0]).compute()
t2 = time.monotonic()
print(f'Sorted in {t2-t1:.2f}s.')

#from IPython import embed
#embed()

