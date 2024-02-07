# do this before running visualize on s3df
# export PYTHONPATH=/sdf/home/m/monarin/sw/lib/python3.9/site-packages:$PYTHONPATH
from mpi4py import MPI
import h5py
import numpy as np
import dask
import dask.array as da
import dask.dataframe as dd
import time


comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.rank  
comm.Barrier()
st = MPI.Wtime()


from dask_jobqueue import SLURMCluster
from dask.distributed import Client, progress
partition = 'milano'  # For LCLS II staff
n_procs = 10

cluster = SLURMCluster(
    queue=partition,
    account="lcls:data",
    local_directory='/sdf/home/m/monarin/tmp/',  # Local disk space for workers to use

    # Resources per SLURM job (per node, the way SLURM is configured on Roma)
    # processes=16 runs 16 Dask workers in a job, so each worker has 1 core & 32 GB RAM.
    processes=n_procs, cores=n_procs, memory='512GB',
    
)
cluster.scale(jobs=1)
cluster.job_script()
client = Client(cluster)
print(f'RANK:{rank} {client=}')


# Read data
t0 = time.monotonic()
ts_chunks = (100000000,)
calib_chunks = (100000000, 10)
in_f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mylargeh5.h5', 'r')
ts_da = da.from_array(in_f['timestamp'], chunks=ts_chunks)
ts = dd.from_array(ts_da, columns=['timestamp'])
calib = da.from_array(in_f['calib'], chunks=calib_chunks)
t1 = time.monotonic()
print(f'RANK:{rank} reading took {t1-t0:.2f}s.')


# Sorting 
ts.sort_values('timestamp')
#ts.visualize(filename='sort.svg')
inds = ts.index.values
t2 = time.monotonic()
print(f'RANK:{rank} {inds.size=} ({inds.size*inds.itemsize/1e6:.2f}MB) {ts_chunks=} {n_procs=} sorting took {t2-t1:.2f}s.')


# Slicing
dask.config.set(**{'array.slicing.split_large_chunks': True})
sorted_ts = ts_da[inds]
sorted_calib = calib[inds]
#sorted_calib.visualize(filename='slicing.svg')
t3 = time.monotonic()
#print(f'RANK:{rank} {sorted_calib.size=} ({sorted_calib.size*sorted_calib.itemsize/1e9:.2f}GB) {calib_chunks=} {n_procs=} slicing took {t3-t2:.2f}s.')

comm.Barrier()
it = MPI.Wtime()
print(f'RANK:{rank} start writing')
#f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/parallel_test.hdf5', 'w', driver='mpio', comm=MPI.COMM_WORLD)
f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/parallel_test.hdf5', 'w')

f.create_dataset('timestamp', data=sorted_ts.compute())
print(f'RANK:{rank} done writing timestamp')
f.create_dataset('calib', data=sorted_calib.compute())
#print(f'RANK:{rank} done writing calib')

f.close()

comm.Barrier()
en = MPI.Wtime()
if rank == 0:
    print(f'Total Time: {en-st:.2f}s. Load/Sort:{it-st:.2f}s. Writing:{en-it:.2f}s.')
