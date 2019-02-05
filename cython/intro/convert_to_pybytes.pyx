# converting char* to PyBytes
# https://stackoverflow.com/questions/50228544/how-do-i-read-a-c-char-array-into-a-python-bytearray-with-cython

from cpython.bytes cimport PyBytes_FromStringAndSize
import os
from libc.stdlib cimport malloc, free
from posix.unistd cimport read
from psana.dgram import Dgram

cdef size_t chunksize = 0x1000000
cdef size_t got = 0
cdef char* chunk = <char *>malloc(chunksize)
cdef int fd = os.open('/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/data-r0001-s00.xtc2', os.O_RDONLY)

config = Dgram(file_descriptor=fd)
got = read(fd, chunk, chunksize)

if got > 0:
    # create PyByteArray object from char*
    view = PyBytes_FromStringAndSize(chunk, chunksize)
    d = Dgram(view=view, config=config, offset=0)
    print(d.seq.service())




