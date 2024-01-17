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

tm1 = time.monotonic()
from dask_jobqueue import SLURMCluster
from dask.distributed import Client, progress
partition = 'milano'  # For LCLS II staff
n_procs = 100

cluster = SLURMCluster(
    queue=partition,
    account="lcls:data",
    local_directory='/sdf/data/lcls/drpsrcf/ffb/users/monarin/tmp/',  # Local disk space for workers to use

    # Resources per SLURM job (per node, the way SLURM is configured on Roma)
    # processes=16 runs 16 Dask workers in a job, so each worker has 1 core & 32 GB RAM.
    cores=n_procs, memory='512GB',
    
)
cluster.scale(jobs=1)
cluster.job_script()
client = Client(cluster)
t0 = time.monotonic()
print(f'RANK:{rank} {client=} setup cluster done in {t0-tm1:.2f}s.')


# Read data
ts_chunks = (10000000,)
calib_chunks = (10000000, 10)
in_f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mylargeh5.h5', 'r')
da_ts = da.from_array(in_f['timestamp'], chunks=ts_chunks)
dd_ts = dd.from_array(da_ts, columns=['timestamp'])
da_calib = da.from_array(in_f['calib'], chunks=calib_chunks)
t1 = time.monotonic()
print(f'RANK:{rank} reading took {t1-t0:.2f}s.')


# Sorting 
# WARNING: not an in-place operation (needs to assign it to another variable)
dd_ts_sorted = dd_ts.sort_values('timestamp')
#ts.visualize(filename='sort.svg')
t2 = time.monotonic()
print(f'RANK:{rank} {ts_chunks=} {n_procs=} sorting took {t2-t1:.2f}s.')


# Load indices
inds = dd_ts_sorted.index.values
t2a = time.monotonic()
print(f'RANK:{rank} compute indices took {t2a-t2:.2f}s.')


# Slicing
slicing_flag = True
if slicing_flag:
    dask.config.set(**{'array.slicing.split_large_chunks': True})
    sorted_ts = da_ts[inds]
    sorted_calib = da_calib[inds]
    #sorted_calib.visualize(filename='slicing.svg')
t3 = time.monotonic()
#print(f'RANK:{rank} {sorted_calib.size=} ({sorted_calib.size*sorted_calib.itemsize/1e9:.2f}GB) {calib_chunks=} {n_procs=} slicing took {t3-t2:.2f}s.')

comm.Barrier()
it = MPI.Wtime()

write_flag = True
if write_flag:
    print(f'RANK:{rank} start writing')
    #f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/parallel_test.hdf5', 'w', driver='mpio', comm=MPI.COMM_WORLD)
    f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/parallel_test.hdf5', 'w')

    f.create_dataset('timestamp', data=sorted_ts.compute())
    print(f'RANK:{rank} done writing timestamp')
    #f.create_dataset('calib', data=sorted_calib.compute())
    #print(f'RANK:{rank} done writing calib')

    f.close()

comm.Barrier()
en = MPI.Wtime()
if rank == 0:
    print(f'Total Time: {en-st:.2f}s. Load/Sort:{it-st:.2f}s. Writing:{en-it:.2f}s.')
