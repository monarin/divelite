from mpi4py import MPI
import h5py
import numpy as np
import dask.array as da
import time


comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.rank  # The process ID (integer 0-3 for 4-process run)
comm.Barrier()
st = MPI.Wtime()


from dask_jobqueue import SLURMCluster
from dask.distributed import Client, progress
partition = 'milano'  # For LCLS II staff

cluster = SLURMCluster(
    queue=partition,
    account="lcls:data",
    local_directory='/sdf/home/m/monarin/tmp/',  # Local disk space for workers to use

    # Resources per SLURM job (per node, the way SLURM is configured on Roma)
    # processes=16 runs 16 Dask workers in a job, so each worker has 1 core & 32 GB RAM.
    processes=10, cores=10, memory='512GB',
)
cluster.scale(jobs=1)
cluster.job_script()
client = Client(cluster)
print(f'RANK:{rank} {client=}')


t0 = time.monotonic()
ts_chunks = (1000000,)
calib_chunks = (1000000, 6)
in_f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mysmallh5.h5', 'r')
ts = da.from_array(in_f['timestamp'], chunks=ts_chunks)
calib = da.from_array(in_f['calib'], chunks=calib_chunks)
t1 = time.monotonic()
print(f'RANK:{rank} reading took {t1-t0:.2f}s.')
inds = ts.argtopk(-ts.shape[0]).compute()
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

print(f'RANK:{rank} start writing')
f.create_dataset('timestamp', data=sorted_ts.compute())
print(f'RANK:{rank} done writing timestamp')
f.create_dataset('calib', data=sorted_calib.compute())
print(f'RANK:{rank} done writing calib')

f.close()

comm.Barrier()
en = MPI.Wtime()
if rank == 0:
    print(f'Total Time: {en-st:.2f}s. Load/Sort:{it-st:.2f}s. Writing:{en-it:.2f}s.')
