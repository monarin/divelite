import os, time, glob, sys
import pstats, cProfile
import pyximport
pyximport.install()
from smdreader import SmdReader
from psana import dgram

def run_smd0():
    filenames = glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/test/smalldata/*.smd.xtc')
    #filenames = glob.glob('/u1/mona/smalldata/*.smd.xtc')
    fds = [os.open(filename, os.O_RDONLY) for filename in filenames]
    # read configs so that fileptr is in the right place
    configs = [dgram.Dgram(file_descriptor=fd) for fd in fds]
    limit = int(sys.argv[1])
    st = time.time()
    smdr = SmdReader(fds[:limit])
    got_events = -1
    n_events = 10000
    processed_events = 0
    while got_events != 0:
        smdr.get(n_events)
        got_events = smdr.got_events
        processed_events += got_events
        #if processed_events >= 100: break
        #print("processed_events: %d"%processed_events)
    en = time.time()
    print("Elapsed Time (s): %f #Events: %d Rate: %f"%((en-st), processed_events, processed_events/((en-st)*1e6)))

if __name__ == "__main__":
    #run_smd0()
    cProfile.runctx("run_smd0()", globals(), locals(), "Profile.prof")
    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("time").print_stats()
