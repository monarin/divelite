from mpi4py import MPI
comm = MPI.COMM_WORLD
group = comm.Get_group() # this is the world group

newgroup = group.Excl([0])

print(dir(newgroup))
newcomm = comm.Create(newgroup)

if comm.rank == 0:
    assert newcomm == MPI.COMM_NULL
else:
    assert newcomm.size == comm.size - 1
    assert newcomm.rank == comm.rank - 1
    print(comm.rank, comm.size, newcomm.rank, newcomm.size)

group.Free()
newgroup.Free()
if newcomm: newcomm.Free()



