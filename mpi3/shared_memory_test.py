from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

import numpy as np

# create a shared array of size 1000 elements of type double
n = 1000
itemsize = MPI.DOUBLE.Get_size()
if rank == 0:
    nbytes = n * itemsize
else:
    nbytes = 0

# on rank 0, create the shared block
# on rank 1, get a handle to it (a window)
win = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm)

# create a numpy array whose data points to the shared mem
buf, itemsize = win.Shared_query(0)
assert itemsize == MPI.DOUBLE.Get_size()
ary = np.ndarray(buffer=buf, dtype='d', shape=(n,))

# in process rank 1:
# write the numbers 0.0,1.0,..,4.0 to the first 5 elements of the array
if rank == 1:
    ary[:5] = np.arange(5)

# wait in process rank 0 until process 1 has written to the array
comm.Barrier()

if rank == 0:
    print(ary[:10])
