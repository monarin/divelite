import h5py
import sys
import numpy as np
import random
from pathlib import Path
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm.Barrier()
st = MPI.Wtime()
import dask.array as da


starting_ts = 4295030300
n_total_images = 1000000000
img_width = 10 
calib_shape = (n_total_images, img_width)

# Create a random timestamps
t0 = time.monotonic()
rng = da.random.default_rng(seed=42)
if rank == 0:
    print(f'RANK:{rank} Generating random indices', flush=True)
    timestamps = rng.integers(low=starting_ts, high=starting_ts+n_total_images, size=n_total_images)
    #timestamps = da.from_array(np.asarray(random.sample(range(starting_ts, starting_ts+n_total_images), n_total_images), dtype=np.int64), chunks='auto')
    #assert len(timestamps) == np.unique(timestamps).shape[0]
else:
    timestamps = None
timestamps = comm.bcast(timestamps, root=0)
t1 = time.monotonic()
print(f'RANK:{rank} {timestamps[:3]=}')
print(f'RANK:{rank} Create random timestamp for {n_total_images} done in {t1-t0:.2f}s.', flush=True)
calib = rng.random(calib_shape)
t2 = time.monotonic()
print(f'RANK:{rank} Create calib {calib.shape} done in {t2-t1:.2f}s.', flush=True)


comm.Barrier()
it = MPI.Wtime()
#f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mylargeh5.h5', 'w', driver='mpio', comm=MPI.COMM_WORLD)
f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mylargeh5.h5', 'w')

f.create_dataset('timestamp', data=timestamps, chunks=True)
print(f'RANK:{rank} done writing timestamp')
f.create_dataset('calib', data=calib, chunks=True)
print(f'RANK:{rank} done writing calib')

f.close()

comm.Barrier()
en = MPI.Wtime()
if rank == 0:
    print(f'Total Time: {en-st:.2f}s Create:{it-st:.2f}s. Writing:{en-it:.2f}s.')
    f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mylargeh5.h5', 'r')
    for key in f.keys():
        print(key, f[key].shape)
    f.close()
