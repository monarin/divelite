from psana.dgram import Dgram
import os

SLOWNESS = 10

file_in = "/reg/neh/home/monarin/psana-nersc/psana2/.tmp/data-r0001-s01.xtc2"
fd = os.open(file_in, os.O_RDONLY)
file_in_size = os.path.getsize(file_in)

f = open("junk.xtc2", "wb")

config = Dgram(file_descriptor=fd)
offset = memoryview(config).nbytes
cn_dgrams = 1
cn_for_slow = 0
f.write(config)
while offset < file_in_size:
    d = Dgram(config=config)
    offset += memoryview(d).nbytes
    write_ok = False
    if d.service() != 12:
        write_ok = True
    else:
        if cn_for_slow == SLOWNESS - 1:
            write_ok = True
            cn_for_slow = 0
        else:
            cn_for_slow += 1
    if write_ok:
        print(memoryview(d).nbytes, d.timestamp(), offset, d.service())
        cn_dgrams += 1
        f.write(d)

print(f'found {cn_dgrams} dgrams')
f.close()
os.close(fd)
