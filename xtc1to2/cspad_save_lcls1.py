import sys

# Modified from cpo example 
# https://github.com/chrisvam/psana_cpo/blob/master/hexanode_save_lcls1.py

if len(sys.argv) == 1:
    print("Usage: ")
    print("source /reg/g/psdm/etc/psconda.sh")
    print("python cspad_save_lcls1.py exp run detname n_events xtc_dir")
    print("note: use n,m for run n to m, -1 for n_events for all events, leave out xtc_dir if using the experiment folder")
    print("ex: python cspad_save_lcls1.py cxid9114 95,114 CxiDs2.0:Cspad.0 -1 /reg/d/psdm/cxi/cxid9114/demo/xtc")
    exit()
            
from psana import *
import numpy as np
import time
exp = sys.argv[1]
run = sys.argv[2]
detname = sys.argv[3]
n_events = int(sys.argv[4])
xtc_dir = None
if len(sys.argv) == 6:
    xtc_dir = sys.argv[5]

if run.find(',') > -1:
    run_range = run.split(',')
    run_st, run_en = int(run_range[0]), int(run_range[1])+1
else:
    run_st = int(run)
    run_en = run_st + 1

for run in range(run_st, run_en):
    #hit_ts = np.loadtxt('hits_r%s.txt'%(str(run).zfill(4)), dtype=np.int)
    if xtc_dir:
        dsource = MPIDataSource('exp=%s:run=%s:dir=%s:smd'%(exp, str(run), xtc_dir))
    else:
        dsource = MPIDataSource('exp=%s:run=%s:smd'%(exp, str(run)))

    det = Detector(detname)
    epics = dsource.env().epicsStore()

    h5fname = "%s_r%d.h5"%(exp, run)
    smldata = dsource.small_data(h5fname, gather_interval=1)
    for nevt,evt in enumerate(dsource.events()):
        raw = det.raw(evt)
        if raw is None: continue 
        photon_energy = epics.value('SIOC:SYS0:ML00:AO541')

        evt_id = evt.get(EventId)
        sec = evt_id.time()[0]
        nsec = evt_id.time()[1]
        timestamp = (sec << 32) | nsec
        
        t = evt_id.time()
        ms = "%03d" % (t[1]/1000000)
        tstring = int(time.strftime("%Y%m%d%H%M%S", time.gmtime(t[0])) + ms)
        #found = np.searchsorted(hit_ts, tstring)
        #if hit_ts[found] == tstring:
        print(run, nevt, raw.shape, photon_energy, timestamp, tstring)
        smldata.event(raws=raw, photon_energies=photon_energy, timestamps=timestamp)

        if n_events > -1:
            if nevt>n_events: break
    
    smldata.save()
    smldata.close()
    print('Done with run %d'%run)
    
