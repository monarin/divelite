import os, glob
import smdreader
smd_files = glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/test/smalldata/*.smd.xtc')
fds = [os.open(smd_file, os.O_RDONLY) for smd_file in smd_files]
smdr=smdreader.SmdReader(file_descriptors=fds)
smdr.get(1000)
