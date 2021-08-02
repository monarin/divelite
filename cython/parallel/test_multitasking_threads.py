from multitasking_threads import run
import os, sys
import numpy as np
import time

xtc_dir     = '/cds/data/drpsrcf/users/monarin/xtcdata/10M60n/xtcdata/smalldata/'
#xtc_dir     = '/cds/data/drpsrcf/users/monarin/xtcdata/smallset/xtcdata/smalldata/'
n_files     = int(sys.argv[1])  
file_names  = [os.path.join(xtc_dir, f'data-r0001-s{str(i).zfill(2)}.smd.xtc2') \
                for i in range(n_files)]
fds         = np.array([os.open(filename, os.O_DIRECT) for filename in file_names], 
                dtype=np.int32)

st = time.monotonic()
run(fds)
en = time.monotonic()
print(f'#Files: {n_files} Elapsed(s): {en-st:.2f}s. Bandwidth(GB/s):{760045608*n_files*1e-9/(en-st):.2f}')
