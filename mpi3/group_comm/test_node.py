import os
from sys import byteorder
import numpy as np
from psana.psexp.smdreader_manager import SmdReaderManager
from psana.psexp.eventbuilder_manager import EventBuilderManager
from psana.psexp.event_manager import EventManager

from mpi4py import MPI
comm = MPI.COMM_WORLD
world_rank = comm.Get_rank()
world_size = comm.Get_size()
group = comm.Get_group() # This this the world group

import glob
from psana import dgram
from psana.dgrammanager import DgramManager

# Setting up group communications
# Ex. PS_SMD_NODES=3 mpirun -n 13
#       1   4   7   10
#   0   2   5   8   11
#       3   6   9   12
#-smd_group-
#       -bd_main_group-
#       color
#       0   0   0   0
#       1   1   1   1
#       2   2   2   2
#       bd_main_rank        bd_rank
#       0   3   6   9       0   1   2   3
#       1   4   7   10      0   1   2   3
#       2   5   8   11      0   1   2   3

PS_SMD_NODES = int(os.environ.get('PS_SMD_NODES', 1))
smd_group = group.Incl(range(PS_SMD_NODES + 1))
bd_main_group = group.Excl([0])

smd_comm = comm.Create(smd_group)
smd_rank = 0
smd_size = 0
if smd_comm != MPI.COMM_NULL:
    smd_rank = smd_comm.Get_rank()
    smd_size = smd_comm.Get_size()

bd_main_comm = comm.Create(bd_main_group)
bd_main_rank = 0
bd_main_size = 0
bd_rank = 0
bd_size = 0
color = 0
nodetype = None
if bd_main_comm != MPI.COMM_NULL:
    bd_main_rank = bd_main_comm.Get_rank()
    bd_main_size = bd_main_comm.Get_size()

    # Split bigdata main comm to PS_SMD_NODES groups
    color = bd_main_rank % PS_SMD_NODES
    bd_comm = bd_main_comm.Split(color, bd_main_rank)
    bd_rank = bd_comm.Get_rank()
    bd_size = bd_comm.Get_size()
    
    if bd_rank == 0:
        nodetype = 'smd'
    else:
        nodetype = 'bd'

if nodetype is None:
    nodetype = 'smd0' # if no nodetype assigned, I must be smd0

#print(world_rank, world_size, smd_rank, smd_size, bd_main_rank, bd_main_size, bd_rank, bd_size, color, nodetype)

class Smd0(object):
    """ Sends blocks of smds to smd_node
    Identifies limit timestamp of the slowest detector then
    sends all smds within that timestamp to an smd_node.
    """
    def __init__(self, fds, max_events=0):
        self.smdr_man = SmdReaderManager(fds, max_events)
        self.run_mpi()

    def run_mpi(self):
        rankreq = np.empty(1, dtype='i')

        for chunk in self.smdr_man.chunks():
            smd_comm.Recv(rankreq, source=MPI.ANY_SOURCE)
            smd_comm.Send(chunk, dest=rankreq[0])

        for i in range(PS_SMD_NODES):
            smd_comm.Recv(rankreq, source=MPI.ANY_SOURCE)
            smd_comm.Send(bytearray(), dest=rankreq[0])

class SmdNode(object):
    """Handles both smd_0 and bd_nodes
    Receives blocks of smds from smd_0 then assembles
    offsets and dgramsizes into a numpy array. Sends
    this np array to bd_nodes that are registered to it."""
    def __init__(self, configs, batch_size=1, filter=0):
        self.eb_man = EventBuilderManager(configs, batch_size, filter)
        self.n_bd_nodes = bd_comm.Get_size() - 1

    def run_mpi(self):
        rankreq = np.empty(1, dtype='i')
        while True:
            # handles requests from smd_0
            smd_comm.Send(np.array([smd_rank], dtype='i'), dest=0)
            info = MPI.Status()
            smd_comm.Probe(source=0, status=info)
            count = info.Get_elements(MPI.BYTE)
            view = bytearray(count)
            smd_comm.Recv(view, source=0)
            if count == 0:
                break
            
            # build batch of events
            for batch in self.eb_man.batches(view):
                bd_comm.Recv(rankreq, source=MPI.ANY_SOURCE)
                bd_comm.Send(batch, dest=rankreq[0])
        
        for i in range(self.n_bd_nodes):
            bd_comm.Recv(rankreq, source=MPI.ANY_SOURCE)
            bd_comm.Send(bytearray(), dest=rankreq[0])


class BigDataNode(object):
    def __init__(self, smd_configs, dm, filter_callback):
        self.evt_man = EventManager(smd_configs, dm, filter_callback)

    def run_mpi(self):
        while True:
            bd_comm.Send(np.array([bd_rank], dtype='i'), dest=0)
            info = MPI.Status()
            bd_comm.Probe(source=0, tag=MPI.ANY_TAG, status=info)
            count = info.Get_elements(MPI.BYTE)
            view = bytearray(count)
            bd_comm.Recv(view, source=0)
            if count == 0:
                break

            for event in self.evt_man.events(view):
                yield event

def run_node(max_events, batch_size, filter_callback):
    
    if nodetype == 'smd0':
        xtc_files = glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/*.xtc2')
        smd_files = glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/smalldata/*.xtc2')
        dm = DgramManager(xtc_files)
        configs = dm.configs
        smd_dm = DgramManager(smd_files)
        smd_configs = smd_dm.configs
        nbytes = np.array([memoryview(config).shape[0] for config in configs], \
                        dtype='i')
        smd_nbytes = np.array([memoryview(config).shape[0] for config in smd_configs], \
                        dtype='i')
    else:
        xtc_files = glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/*.xtc2')
        smd_files = glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/smalldata/*.xtc2')
        dm = None
        smd_dm = None
        nbytes = np.empty(len(xtc_files), dtype='i')
        smd_nbytes = np.empty(len(smd_files), dtype='i')

    comm.Bcast(smd_nbytes, root=0) # no. of bytes is required for mpich and creating empty dgram
    comm.Bcast(nbytes, root=0)

    # create empty dgrams of known size
    if nodetype in ('smd', 'bd'):
        smd_configs = [dgram.Dgram(size=smd_nbyte) for smd_nbyte in smd_nbytes]
        configs = [dgram.Dgram(size=nbyte) for nbyte in nbytes]

    for i in range(len(smd_files)):
        comm.Bcast([smd_configs[i], smd_nbytes[i], MPI.BYTE], root=0)

    for i in range(len(xtc_files)):
        comm.Bcast([configs[i], nbytes[i], MPI.BYTE], root=0)
    
    if nodetype in ('smd', 'bd'):
        smd_dm = DgramManager(smd_files, configs=smd_configs)
        dm = DgramManager(xtc_files, configs=configs)

    if nodetype == 'smd0':
        Smd0(smd_dm.fds, max_events=max_events)
    elif nodetype == 'smd':
        smd_node = SmdNode(smd_configs, batch_size=batch_size, filter=filter_callback)
        smd_node.run_mpi()
    elif nodetype == 'bd':
        bd_node = BigDataNode(smd_configs, dm, filter_callback)
        for evt in bd_node.run_mpi():
            yield evt

def filter_fn(evt):
    pass

if __name__ == "__main__":
    max_events = 10000
    batch_size = 1000
    filter_callback = 0
    for i in run_node(max_events, batch_size, filter_fn):
        print(i)
