# write cmd: python collective_io.py w 100000000
# read cmd: mpirun -n 10 python collective_io.py r 100000000
from mpi4py import MPI
import numpy as np
import sys, time, os

mode = sys.argv[1]
file_name = "/reg/d/psdm/cxi/cxid9114/scratch/mona/datafile.config"

comm = MPI.COMM_WORLD
if mode == "w":
    if comm.Get_rank() == 0:
        if os.path.isfile(file_name):
            os.remove(file_name)
            print("remove %s"%file_name)

if mode == "w":
    amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
elif mode == "r":
    amode = MPI.MODE_RDONLY

fh = MPI.File.Open(comm, file_name, amode)

comm.Barrier()
start = MPI.Wtime()

n = int(sys.argv[2])
buffer = np.empty( int(n / comm.Get_size()), dtype=np.int)

if mode == "w":
    buffer[:] = comm.Get_rank()

offset = comm.Get_rank() * buffer.nbytes

if mode == "r":
    fh.Read_at_all(offset, buffer)
elif mode == "w":
    fh.Write_at_all(offset, buffer)

comm.Barrier()
end = MPI.Wtime()

fh.Close()

statinfo = os.stat(file_name)
if comm.Get_rank() == 0: 
    print(buffer.size)
    print("Time (s):", end-start, "Bandwidth (GB/s):", (statinfo.st_size*1e-9)/(end-start))

if mode == "r":
    if comm.Get_rank() == 0:
        start = time.time()
        with open(file_name,'r') as f:
            read_data = f.read()
        end = time.time()
        print("Python open-read time(s):", end-start, "Bandwidth (GB/s):", (statinfo.st_size*1e-9)/(end-start))
