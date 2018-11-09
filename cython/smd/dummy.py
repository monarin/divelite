from smdreader import DummyReader
import os, glob, sys, time
from psana import dgram

#xtc_files = glob.glob("/reg/d/psdm/xpp/xpptut15/scratch/mona/test/smalldata/data-*.smd.xtc")
#xtc_files = glob.glob(".tmp/smalldata/data-*.smd.xtc")
xtc_files = glob.glob("/ffb01/monarin/test/smalldata/data-*.smd.xtc")
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

