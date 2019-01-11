#from smdreader import DummyReader
from psana.smdreader import SmdReader as DummyReader
import os, glob, sys, time
from psana import dgram

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    #xtc_files = glob.glob("/reg/d/psdm/xpp/xpptut15/scratch/mona/test/smalldata/data-*.smd.xtc")
    #xtc_files = glob.glob(".tmp/smalldata/data-*.smd.xtc")
    #xtc_files = glob.glob("/ffb01/monarin/hsd/smalldata/data-*.smd.xtc")
    #xtc_files = glob.glob("/global/cscratch1/sd/monarin/testxtc2/hsd/smalldata/data-*.smd.xtc")
    xtc_files = glob.glob("/var/opt/cray/dws/mounts/batch/psana2_hsd_16718487_striped_scratch/hsd/smalldata/data-*.smd.xtc")
    if not xtc_files:
        print("smd files not found.")
        exit()

    n_files = int(sys.argv[1])
    fds = [os.open(xtc_file, os.O_RDONLY) for xtc_file in xtc_files]

    # do this to move to dgram part of the xtc
    # since config doesn't have correct timestamp so the 
    # code won't work - won't happen in real situation
    configs = [dgram.Dgram(file_descriptor=fd) for fd in fds]

    st = time.time()
    smdr = DummyReader(fds[:n_files])
    got_events = -1
    processed_events = 0
    while got_events != 0:
        smdr.get(1000)
        got_events = smdr.got_events
        processed_events += got_events
        for i in range(n_files):
            view = smdr.view(i)
        #if processed_events >= 1000: break

    en = time.time()
    print("processed_events %d total elapsed %f s rate %f MHz"%(processed_events, en-st, processed_events/((en-st) * 1000000)))
    #print("DeltaT get_init(s): %f"%(smdr.dt_get_init))
    #print("DeltaT get_dgram(s): %f"%(smdr.dt_get_dgram))
    #print("DeltaT reread(s): %f"%(smdr.dt_reread))
    total = en-st
    print(total)
    print(smdr.dt_get_init)
    #print(smdr.dt_sub_reread)
    print(smdr.dt_reread)
    print(total - smdr.dt_get_init - smdr.dt_reread)

