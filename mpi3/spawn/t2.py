from mpi4py import MPI

comm = MPI.Comm.Get_parent()

print ('ho ', comm.Get_rank(), ' of  ',comm.Get_size(),' ', MPI.COMM_WORLD.Get_rank(), ' of  ',MPI.COMM_WORLD.Get_size())
a = MPI.COMM_WORLD.bcast(MPI.COMM_WORLD.Get_rank(), root=0)
print ("value from other child", a)

print ("comm.Is_inter", comm.Is_inter())
b = comm.bcast(comm.Get_rank(), root=0)
print ("value from parent", b)

common_comm=comm.Merge(True)
print ("common_comm.Is_inter", common_comm.Is_inter())
print ('common_comm ', common_comm.Get_rank(), ' of  ',common_comm.Get_size())

c=common_comm.bcast(0, root=0)
print ("value from rank 0 in common_comm", c)
