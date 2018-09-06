from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

import numpy as np
from queue import Queue

def smd_0(n_smd_nodes):
    rankreq = np.empty(1, dtype='i')
    for i in range(1000):
        comm.Recv(rankreq, source=MPI.ANY_SOURCE)
        comm.Send(b'hello', dest=rankreq[0], tag=12)

    for i in range(n_smd_nodes):
        comm.Recv(rankreq, source=MPI.ANY_SOURCE)
        comm.Send(bytearray(b'eof'), dest=rankreq[0], tag=12)

def smd_node(n_bd_nodes):
    rankreq = np.empty(1, dtype='i')
    view = 0
    while True:
        if not view:
            comm.Send(np.array([rank], dtype='i'), dest=0)
            info = MPI.Status()
            comm.Probe(source=0, tag=12, status=info)
            count = info.Get_elements(MPI.BYTE)
            view = bytearray(count)
            comm.Recv(view, source=0, tag=12)
            if view.startswith(b'eof'):
                break
            print("smd_node", rank, 'received', view)
        else:
            # resend to bd_node
            comm.Recv(rankreq, source=MPI.ANY_SOURCE, tag=13)
            comm.Send(view, dest=rankreq[0])
            view = 0

    for i in range(n_bd_nodes):
        comm.Recv(rankreq, source=MPI.ANY_SOURCE, tag=13)
        comm.Send(bytearray(b'eof'), dest=rankreq[0])


def bd_node(smd_node_id):
    while True:
        comm.Send(np.array([rank], dtype='i'), dest=smd_node_id, tag=13)
        info = MPI.Status()
        comm.Probe(source=smd_node_id, tag=MPI.ANY_TAG, status=info)
        count = info.Get_elements(MPI.BYTE)
        view = bytearray(count)
        comm.Recv(view, source=smd_node_id)
        if view.startswith(b'eof'):
            break
        print("  bd_node", rank, view)


if __name__ == "__main__":
    n_smd_nodes = int(round((size - 1) * .25))
    n_bd_nodes = size - 1 - n_smd_nodes
    if rank == 0:
        smd_0(n_smd_nodes)
    elif rank < n_smd_nodes + 1:
        clients = (np.arange(size)[n_smd_nodes+1:] % n_smd_nodes) + 1
        smd_node(len(clients[clients==rank]))
    else:
        smd_node_id = (rank % n_smd_nodes) + 1
        bd_node(smd_node_id)

