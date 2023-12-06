from mpi4py import MPI
import h5py
import numpy as np
import dask.array as da
import time


comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.rank  # The process ID (integer 0-3 for 4-process run)
comm.Barrier()
st = MPI.Wtime()


t0 = time.monotonic()
in_f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mysmallh5.h5', 'r')
ts = da.from_array(in_f['timestamp'], chunks='auto')
calib = da.from_array(in_f['calib'], chunks='auto')
t1 = time.monotonic()
print(f'RANK:{rank} reading took {t1-t0:.2f}s.')
inds = ts.argtopk(-ts.shape[0])
t2 = time.monotonic()
print(f'RANK:{rank} sorting took {t2-t1:.2f}s.')
sorted_ts = ts[inds]
sorted_calib = calib[inds]
t3 = time.monotonic()
print(f'RANK:{rank} slicing took {t3-t2:.2f}s.')

comm.Barrier()
it = MPI.Wtime()
#f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/parallel_test.hdf5', 'w', driver='mpio', comm=MPI.COMM_WORLD)
f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/parallel_test.hdf5', 'w')

f.create_dataset('timestamp', data=sorted_ts)
f.create_dataset('calib', data=sorted_calib)

f.close()

comm.Barrier()
en = MPI.Wtime()
if rank == 0:
    print(f'Total Time: {en-st:.2f}s. Load/Sort:{it-st:.2f}s. Writing:{en-it:.2f}s.')
