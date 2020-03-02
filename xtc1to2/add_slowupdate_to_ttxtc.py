from psana.dgram import Dgram
import os
import dgramCreate as dc
from psana import DataSource
import numpy as np

SLOWUPDATE_FREQ = 100 # every 100 L1 , insert one slowupdate (with 0 array for fake bg)

file_in = "/reg/neh/home/monarin/lcls2/psana/psana/tests/test_timetool.xtc2"
fd = os.open(file_in, os.O_RDONLY)
file_in_size = os.path.getsize(file_in)
ds = DataSource(files=file_in)
run = next(ds.runs())

f = open("junk.xtc2", "wb")

# tmodet
detname = 'tmott'
dettype = 'ttdet'
serial_number = 'tt_detector_identification_placeholder'
namesid = 0
nameinfo = dc.nameinfo(detname,dettype,serial_number,namesid)
alg = dc.alg('ttalg',[0,0,1])
cydgram = dc.CyDgram()
data = {'data': np.zeros((4272,), dtype=np.uint8)}
cydgram.addDet(nameinfo, alg, data)

# runinfo detector
runinfo_detname = 'runinfo'
runinfo_dettype = 'runinfo'
runinfo_detid = ''
runinfo_namesid = 1
runinfo_nameinfo = dc.nameinfo(runinfo_detname, runinfo_dettype,
        runinfo_detid, runinfo_namesid)
runinfo_alg = dc.alg('runinfo', [0,0,1])
runinfo_data = {
        'expt': 'tmo',
        'runnum': 1
        }
cydgram.addDet(runinfo_nameinfo, runinfo_alg, runinfo_data)

# epics detector for storing IIR bg
epics_detname = 'epics'
epics_dettype = 'epics'
epics_detid = ''
epics_namesid = 2
epics_nameinfo = dc.nameinfo(epics_detname, epics_dettype,
        epics_detid, epics_namesid)
epics_alg = dc.alg('epics', [0,0,0])
epics_data = {'IIR': np.zeros((2048,), dtype=np.uint8)}
cydgram.addDet(epics_nameinfo, epics_alg, epics_data)

# Write configure
xtc_bytes = cydgram.get(0, 2) # timestamp and Configure transitionId
f.write(xtc_bytes)

# Write beginRun
cydgram.addDet(nameinfo, alg, data)
cydgram.addDet(runinfo_nameinfo, runinfo_alg, runinfo_data)
xtc_bytes = cydgram.get(1, 4) # timestamp and BeginRun transitionId
f.write(xtc_bytes)

det = run.Detector('tmott')
cn_ts = 2
cn_L1 = 0
cn_SlowUpdate = 0
for nevt, evt in enumerate(run.events()):
    data = {'data': det.ttalg._image(evt)}

    cydgram.addDet(nameinfo, alg, data)
    xtc_bytes = cydgram.get(cn_ts, 12) # timestamp and L1 transitionId
    f.write(xtc_bytes)
    cn_ts += 1
    cn_L1 += 1
    
    # add slowupdate every SLOWUPDATE_FREQ
    if nevt % SLOWUPDATE_FREQ == 0:
        print(f'adding slowupdate after this {cn_ts}')
        cydgram.addDet(epics_nameinfo, epics_alg, epics_data)
        xtc_bytes = cydgram.get(cn_ts, 10) 
        f.write(xtc_bytes)
        cn_ts += 1
        cn_SlowUpdate += 1

print(f'wrote {cn_L1} L1 {cn_SlowUpdate} SlowUpdate Total {cn_ts-2}')

f.close()
os.close(fd)
