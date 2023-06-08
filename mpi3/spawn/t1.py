from mpi4py import MPI
import sys

sub_comm = MPI.COMM_SELF.Spawn(sys.executable, args=['t2.py'], maxprocs=3)

val=42
sub_comm.bcast(val, MPI.ROOT)

common_comm=sub_comm.Merge(False)
print ('parent in common_comm ', common_comm.Get_rank(), ' of  ',common_comm.Get_size())
#MPI_Intercomm_merge(parentcomm,1,&intracomm);

val=13
c=common_comm.bcast(val, root=0)
print ("value from rank 0 in common_comm", c)
