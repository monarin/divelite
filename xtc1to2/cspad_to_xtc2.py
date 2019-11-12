import h5py
import os, sys, glob
import dgramCreate as dc

# Get data from h5 file
h5f_names = []
for i in range(95,114+1):
    h5f_names.append(os.path.join('.',f'cxid9114_r{i}.h5'))

# Create a config
config = {}
detname = 'cspad'
dettype = 'cspad'
serial_number = '1234'
namesid = 0

nameinfo = dc.nameinfo(detname, dettype, serial_number, namesid)
alg = dc.alg('raw', [1,2,3])

cydgram = dc.CyDgram()


# Prepare output file
fname = sys.argv[1]
f = open(fname, 'wb')


# Add data
cn_events = 0
for h5f_name in h5f_names:
    h5f = h5py.File(h5f_name)
    raws = h5f['raws']
    photon_energies = h5f['photon_energies']
    timestamps = h5f['timestamps']

    for nevt, (raw, photon_energy, timestamp) in enumerate(zip(raws, photon_energies, timestamps)):
        my_data = {
                'raw': raw,
                'photonEnergy': photon_energy
        }

        cydgram.addDet(nameinfo, alg, my_data)
        pulseid = timestamp
        flag_write_ok = True
        if (nevt == 0):
            if (cn_events == 0):
                transitionid = 2 # Configure
            else:
                transitionid = 12 # L1Accept
        else:
            transitionid = 12 # L1Accept
        
        xtc_bytes = cydgram.get(timestamp, pulseid, transitionid)
        f.write(xtc_bytes)
        cn_events += 1
        #print(cn_events, raw.shape, photon_energy, timestamp)

f.close()


