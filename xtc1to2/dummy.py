from psana import DataSource

#xtc_dir = "./data"
#xtc_dir = "/reg/neh/home/monarin/lcls2/.tmp"
xtc_dir ="."

from psana.dgrammanager import DgramManager
import os
dm = DgramManager(os.path.join(xtc_dir, 'out.xtc2'))
cfg_dgram = dm.configs[0]
#print(dir(cfg_dgram))
for det_name, det_dict in cfg_dgram.software.__dict__.items():
    first_key = next(iter(det_dict.keys()))
    det = det_dict[first_key]
    for drp_class_name, drp_class in det.__dict__.items():
        if drp_class_name in ['dettype', 'detid']: continue
        if drp_class_name.startswith('_'): continue
        versionstring = [str(v) for v in drp_class.version]
        class_name = '_'.join([det.dettype, drp_class.software] + versionstring)
        #print(versionstring, class_name)

ds = DataSource(files='out.xtc2')

for run in ds.runs():
    det = run.Detector('cspad')
    for evt in run.events():
        photon_energy = det.raw.photonEnergy(evt)
        raw = det.raw.raw(evt)
        print(evt.timestamp, photon_energy, raw.shape)



