import numpy
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

randNum = numpy.zeros(1)
diffNum = numpy.random.random_sample(1)

if rank == 1:
    randNum = numpy.random.random_sample(1)
    print("process", rank, "drew the number", randNum[0])
    comm.Isend(randNum, dest=0)
    diffNum /= 3.14 # overlap communication
    print("diffNum=", diffNum[0])
    req = comm.Irecv(randNum, source=0)
    req.Wait()
    print("process", rank, "received the number", randNum[0])

if rank == 0:
    print("process", rank, "before receiving has the number", randNum[0])
    req = comm.Irecv(randNum, source=1)
    req.Wait()
    print("process", rank, "received the number", randNum[0])
    randNum *= 2
    comm.Isend(randNum, dest=1)

