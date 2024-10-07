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
import tables as tb


starting_ts = 4295030300
n_total_images = 100000
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
output_fname = '/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/myrealh5.h5'
#f = h5py.File(output_fname, 'w', driver='mpio', comm=MPI.COMM_WORLD)
f = h5py.File(output_fname, 'w')

f.create_dataset('timestamp', data=timestamps, chunks=True)
print(f'RANK:{rank} done writing timestamp')
f.create_dataset('calib', data=calib, chunks=True)
print(f'RANK:{rank} done writing calib')

# Creates groups to mimic 'real' hdf5
grp1 = f.create_group("/grp1/subgrp1")
print(f'create group: {grp1.name}')
grp1['unaligned_data'] = np.ones((100, 20))
grp1['var_len_str'] = 'hello'
grp1['calib'] = calib

f.close()

comm.Barrier()
en = MPI.Wtime()
if rank == 0:
    print(f'Total Time: {en-st:.2f}s Create:{it-st:.2f}s. Writing:{en-it:.2f}s.')
    h5file = tb.open_file(output_fname,'r')
    for array in h5file.walk_nodes('/', 'Array'):
        print(array, type(array))
    tb.close()
