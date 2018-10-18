from parallel_reader import ParallelReader
import os
import glob

print('python_pid', os.getpid())
smd_files = glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/test/smalldata/*.smd.xtc')
fds = [os.open(smd_file, os.O_RDONLY) for smd_file in smd_files]
print(fds)
pr = ParallelReader(fds)
pr.get()

