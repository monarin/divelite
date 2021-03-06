import dgramCreate as dc
from psana import DataSource
import numpy as np
import os

def test_py2xtc(tmp_path):

    config = {}
    detname = 'cspad'
    dettype = 'cspad'
    serial_number = '1234'
    namesid = 0

    nameinfo = dc.nameinfo(detname,dettype,serial_number,namesid)
    alg = dc.alg('raw',[1,2,3])

    cydgram = dc.CyDgram()

    image_array = np.array([[1,2,3,4],[9,8,7,6]])
    orientations_array = np.array([4,3,2,1])

    runinfo_detname = 'runinfo'
    runinfo_dettype = 'runinfo'
    runinfo_detid = ''
    runinfo_namesid = 1
    runinfo_nameinfo = dc.nameinfo(runinfo_detname,runinfo_dettype,
                                   runinfo_detid,runinfo_namesid)
    runinfo_alg = dc.alg('runinfo',[0,0,1])
    runinfo_data = {
        'expt': 'cxid9114',
        'runnum': 95
    }

    fname = os.path.join(tmp_path,'junk.xtc2')

    f = open(fname,'wb')


    xtc_file = "/gpfs/alpine/proj-shared/chm137/data/LD91/old_data.xtc2"
    ds = DataSource(files=xtc_file)
    run = next(ds.runs())
    det = run.Detector('cspad')
    for i, evt in enumerate(run.events()):
        my_data = {
            'raw': det.raw.raw(evt),
            'photonEnergy': det.raw.photonEnergy(evt)
        }

        cydgram.addDet(nameinfo, alg, my_data)
        # only do this for the first two dgrams: name info for config, and
        # the runinfo data for beginrun
        if i<2: cydgram.addDet(runinfo_nameinfo, runinfo_alg, runinfo_data)
        timestamp = i
        if (i==0):
            transitionid = 2  # Configure
        elif (i==1):
            transitionid = 4  # BeginRun
        else:
            transitionid = 12 # L1Accept
        xtc_bytes = cydgram.get(timestamp,transitionid)
        f.write(xtc_bytes)

        if i == 10: break

    f.close()

    ds = DataSource(files=fname)
    myrun = next(ds.runs())
    assert myrun.expt==runinfo_data['expt']
    assert myrun.runnum==runinfo_data['runnum']
    for nevt,evt in enumerate(myrun.events()):
        assert evt._dgrams[0].cspad[0].raw.raw.shape == (32, 185, 388)
    
    assert nevt>0 #make sure we get events

if __name__ == "__main__":
    import pathlib
    test_py2xtc(pathlib.Path('.'))
