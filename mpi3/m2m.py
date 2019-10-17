import os
import numpy as np

from mpi4py import MPI
comm = MPI.COMM_WORLD
world_rank = comm.Get_rank()
world_size = comm.Get_size()
group = comm.Get_group() # This this the world group

# Setting up group communications
# Ex. PS_SMD_NODES=3 mpirun -n 13
# smd_group:
#       1   
#   0   2   
#       3   
# Each bd node is connected to all eventbuilder nodes
# bd_group 1:
#       1   
#       2   4
#       3   

PS_SMD_NODES = int(os.environ.get('PS_SMD_NODES', 3))
smd_group = group.Incl(range(PS_SMD_NODES + 1))

smd_comm = comm.Create(smd_group)
smd_rank = 0
smd_size = 0
if smd_comm != MPI.COMM_NULL:
    smd_rank = smd_comm.Get_rank()
    smd_size = smd_comm.Get_size()
    print('smd rank=%d size=%d world_rank=%d world_size=%d'%(smd_rank, smd_size, world_rank, world_size))

bd_comms = []
for i in range(PS_SMD_NODES+1, world_size):
    bd_group = group.Incl([i] + list(range(1, PS_SMD_NODES + 1)))
    bd_comm = comm.Create(bd_group)
    bd_comms.append(bd_comm)
    if bd_comm != MPI.COMM_NULL:
        bd_rank = bd_comm.Get_rank()
        bd_size = bd_comm.Get_size()
        print('bd_group_%d: bd rank=%d size=%d world_rank=%d world_size=%d'%(i, bd_rank, bd_size, world_rank, world_size))

class Smd0(object):

    def __init__(self):
        self.run_mpi()

    def run_mpi(self):
        rankreq = np.empty(1, dtype='i')
        data = np.tile(range(4,world_size), 10)

        for d in data:
            smd_comm.Recv(rankreq, source=MPI.ANY_SOURCE)
            smd_comm.Send(int(d).to_bytes(4, byteorder='little'), dest=rankreq[0])

        for i in range(PS_SMD_NODES):
            smd_comm.Recv(rankreq, source=MPI.ANY_SOURCE)
            smd_comm.Send(bytearray(), dest=rankreq[0])

class SmdNode(object):
    def __init__(self): pass

    def run_mpi(self):
        timedelay = np.empty(1, dtype='i')
        while True:
            # Request data from smd0
            smd_comm.Send(np.array([smd_rank], dtype='i'), dest=0)
            info = MPI.Status()
            smd_comm.Probe(source=0, status=info)
            count = info.Get_elements(MPI.BYTE)
            chunk = bytearray(count)
            smd_comm.Recv(chunk, source=0)
            if count == 0:
                break
            
            ichunk = int.from_bytes(chunk, byteorder='little')
            print('Smd%d received %d bytes value=%d'%(smd_rank, count, ichunk))
            
            # Request timedelay from bigdata nodes then send
            # the matching timedelay to the nodes.
            for i, bd_comm in enumerate(bd_comms):
                bd_comm.Send(np.array([bd_comm.Get_rank()], dtype='i'), dest=0)
                bd_comm.Recv(timedelay, source=MPI.ANY_SOURCE)
                
                # Query the received timedelay
                #if ichunk == timedelay[0]:
                #    print('Smd%d send %d to bd_comm_%d'%(bd_comm.Get_rank(), ichunk, i))
                #    bd_comm.Send(chunk, dest=0)

class BigDataNode(object):
    def __init__(self): 
        self.run_mpi()

    def run_mpi(self):
        rankreq = np.empty(1, dtype='i')
        n_data_points = 0

        while True:
            # Get my communicator
            bd_comm = bd_comms[world_rank - (PS_SMD_NODES + 1)]

            # Get an eventbuilder and send it my timedelay
            bd_comm.Recv(rankreq, source=MPI.ANY_SOURCE)
            print("bd_comm_%d received request from rank %d"%(world_rank-(PS_SMD_NODES+1), rankreq[0]))
            bd_comm.Send(np.array([world_rank], dtype='i'), dest=rankreq[0])
            print("bd_comm_%d send timedelay %d to rank %d"%(world_rank-(PS_SMD_NODES+1), world_rank, rankreq[0]))

            # Receive my timedelay-selected data
            """
            info = MPI.Status()
            bd_comm.Probe(source=rankreq[0], status=info)
            count = info.Get_elements(MPI.BYTE)
            chunk = bytearray(count)
            bd_comm.Recv(chunk, source=rankreq[0])
            print('BigData%d received %d bytes value=%d'%(bd_comm.Get_rank(), count, int.from_bytes(chunk, byteorder='little')))
            """

            n_data_points += 1
            if n_data_points == 2:
                break




if __name__ == "__main__":
    if world_rank == 0:
        Smd0()
    elif world_rank < PS_SMD_NODES + 1:
        smd_node = SmdNode()
        smd_node.run_mpi()
    #else: 
    #    BigDataNode()
