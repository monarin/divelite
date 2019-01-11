import os, sys, time
from psana import DataSource
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
myhost = MPI.Get_processor_name()

def filter_fn(evt):
    return True

xtc_dir = "/global/cscratch1/sd/monarin/testxtc2/hsd"
max_events = int(sys.argv[1])
ds = DataSource('exp=xpptut13:run=1:dir=%s'%(xtc_dir), filter=filter_fn, max_events=max_events, batch_size=1)

st = MPI.Wtime()
for run in ds.runs():
    #det = run.Detector('xppcspad')
    for evt in run.events():
<<<<<<< HEAD
        print("%s %d %f"%(myhost, rank, time.time())) 
        #pass
=======
<<<<<<< HEAD
        #print("%s %d %f"%(myhost, rank, time.time())) 
        #print(evt._size)
        pass
=======
        print("%s %d %f"%(myhost, rank, time.time())) 
        #pass
>>>>>>> some changes from NERSC
>>>>>>> e069b000972da00703c13312cbac3a9e8022279b

en = MPI.Wtime()

if rank == 0:
    print("#Events %d #Files %d #smd0_threads %s Total Elapsed (s): %6.2f Rate (kHz): %6.2f"%(max_events, 16, os.environ.get("PS_SMD0_THREADS", 1), en-st, (max_events/((en-st)*1000))))
