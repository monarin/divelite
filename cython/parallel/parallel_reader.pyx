from cython.parallel import parallel, prange
from libc.stdlib cimport abort, malloc, free
from posix.unistd cimport read

cdef struct Buffer:
    char* chunk
    size_t got

cdef class ParallelReader:
    cdef size_t chunksize
    cdef int nfiles
    cdef int* fds
    cdef Buffer *bufs

    def __init__(self, fds):
        self.chunksize = 0x1000000
        self.nfiles = len(fds)
        self.fds = <int *>malloc(sizeof(int) * self.nfiles)
        for i in range(self.nfiles):
            self.fds[i] = fds[i]
        self.bufs = NULL

    def __dealloc__(self):
        if self.bufs:
            for i in range(self.nfiles):
                free(self.bufs[i].chunk)
            free(self.bufs)

    cdef void _init_buffers(self):
        cdef int i
        for i in prange(self.nfiles, nogil=True):
        #for i in range(self.nfiles):
            self.bufs[i].chunk = <char *>malloc(self.chunksize)
            self.bufs[i].got = read(self.fds[i], self.bufs[i].chunk, self.chunksize)
            self.bufs[i].got = read(self.fds[i], self.bufs[i].chunk, self.chunksize)

    def get(self):
        if not self.bufs:
            self.bufs = <Buffer *>malloc(sizeof(Buffer) * self.nfiles)
            self._init_buffers()
        
        cdef int i, local_limit_ts, s
        with nogil, parallel():
            local_limit_ts = 1
            
            for i in prange(self.nfiles, schedule='guided'):
                self.bufs[i].got = read(self.fds[i], self.bufs[i].chunk, self.chunksize)
                self.bufs[i].got = read(self.fds[i], self.bufs[i].chunk, self.chunksize)
                s += local_limit_ts

        print('s=%d'%s)

