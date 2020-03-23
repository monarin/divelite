import dgramCreate as dc
from psana import DataSource
import numpy as np
import os


def collect_dgrams(n_dgrams, seed_file):
    print(f"Collecting {n_dgrams} from {seed_file}") 
    ds = DataSource(files=xtc_file)
    run = next(ds.runs())
    det = run.Detector('cspad')
    dgrams = []
    for i, evt in enumerate(run.events()):
        my_data = {
            'raw': det.raw.raw(evt),
            'photonEnergy': det.raw.photonEnergy(evt)
        }
        dgrams.append(my_data)
        print(f'  saving {i} ts={evt.timestamp}')
        if i == n_dgrams - 1: break
    return dgrams


def extend_xtc(tmp_path, seed_dgrams, n_total_dgrams):
    print(f"Writing out {n_total_dgrams} from {len(seed_dgrams)} seeded dgrams")
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

    i = 0
    cn_seed_dgrams = 0
    while i < n_total_dgrams:
        if cn_seed_dgrams == len(seed_dgrams):
            cn_seed_dgrams = 0

        my_data = seed_dgrams[cn_seed_dgrams]
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
        
        cn_seed_dgrams += 1
        i += 1

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
    #xtc_file = "/gpfs/alpine/proj-shared/chm137/data/LD91/old_data.xtc2"
    xtc_file = "/reg/d/psdm/xpp/xpptut15/scratch/mona/old_data.xtc2"
    seed_dgrams = collect_dgrams(10, xtc_file)
    extend_xtc(pathlib.Path('.'), seed_dgrams, 100)
