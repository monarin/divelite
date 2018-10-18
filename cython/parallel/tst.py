import os, time, glob, sys
from psana.dgrammanager import DgramManager

filenames = glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/test/smalldata/*.smd.xtc')

dm = DgramManager(filenames)
cn_evt = 0
for evt in dm:
    print('evt %d'%cn_evt)
    for d in evt:
        print(d.seq.timestamp())
    cn_evt += 1
    if cn_evt == 2: break
