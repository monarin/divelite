# do this before running visualize on s3df
# export PYTHONPATH=/sdf/home/m/monarin/sw/lib/python3.9/site-packages:$PYTHONPATH
from mpi4py import MPI
import sys
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


# Setup cluster for dask
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
in_f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mylargeh5.h5', 'r')
da_ts = da.from_array(in_f['timestamp'], chunks=ts_chunks)
dd_ts = dd.from_array(da_ts, columns=['timestamp'])
t1 = time.monotonic()
print(f'RANK:{rank} reading took {t1-t0:.2f}s.')


# Sorting 
# WARNING sort_values is not in-place (need to assign the result to another variable)
dd_ts_sorted = dd_ts.sort_values('timestamp')
#ts.visualize(filename='sort.svg')
t2 = time.monotonic()
print(f'RANK:{rank} {ts_chunks=} {n_procs=} sorting took {t2-t1:.2f}s.')


# Load indices
inds = dd_ts_sorted.index.values
inds_arr = np.asarray(inds.compute(), dtype=np.int64)
t2a = time.monotonic()
print(f'RANK:{rank} {inds_arr.size=} ({inds_arr.size*inds_arr.itemsize/1e6:.2f}MB) compute indices took {t2a-t2:.2f}s.')


comm.Barrier()
it = MPI.Wtime()
# Spawn mpiworkers
maxprocs = 200
sub_comm = MPI.COMM_SELF.Spawn(sys.executable, args=['parallel_h5_write.py'], maxprocs=maxprocs)
common_comm=sub_comm.Merge(False)


# Send data
n_samples = inds_arr.shape[0]
batch_size = 10000000
n_files = int(np.ceil(n_samples/batch_size))
rankreq = np.empty(1, dtype='i')
for i in range(n_files):
    st = i * batch_size
    en = st + batch_size
    if en > n_samples: en = n_samples
    common_comm.Recv(rankreq, source=MPI.ANY_SOURCE)
    common_comm.Send(inds_arr[st:en], tag=i, dest=rankreq[0])


# Kill clients
for i in range(common_comm.Get_size()-1):
    common_comm.Recv(rankreq, source=MPI.ANY_SOURCE)
    common_comm.Send(bytearray(), dest=rankreq[0])


comm.Barrier()
en = MPI.Wtime()
print (f"ALL DONE batch_size:{batch_size} maxprocs:{maxprocs} Sort:{it-st:.2f}s. Write:{en-it:.2f}s. Total:{en-st:.2f}s.")
