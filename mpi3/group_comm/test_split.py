from mpi4py import MPI
comm = MPI.COMM_WORLD

world_rank = comm.Get_rank()
world_size = comm.Get_size()

color = int(world_rank /3)


newcomm = comm.Split(color, world_rank)
print(world_rank, world_size, newcomm.Get_rank(), newcomm.Get_size())

newcomm.Free()
