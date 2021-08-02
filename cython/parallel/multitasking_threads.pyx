"""
Performing two tasks:
    1. Reading files to fill out buffers
    2. Reading the buffers and do some computation
Each task will have a group of threads working on it.

Test with:
    python setup.py build_ext --inplace
    python -c "import multitasking_threads"
"""

from cython.parallel import parallel, prange, threadid
from libc.stdlib cimport abort, malloc, free
from libc.string cimport memcpy
from posix.unistd cimport read, sleep
cimport openmp
from libc.stdint cimport uint32_t, uint64_t, int64_t

def run(int[:] fds):
    # Fast indexing
    cdef Py_ssize_t idx, i

    # Buffer settings
    cdef int n_bufs = fds.shape[0] 
    cdef uint64_t buf_size = 100000000
    cdef uint64_t buf_total_size = buf_size * n_bufs
    cdef uint64_t offsets[1000]

    # Read settings
    cdef uint64_t read_size = 5000000
    cdef int64_t gots[1000]
    cdef int dones[1000]
    cdef uint64_t total_gots[1000]
    
    # No. of pools of threads
    cdef int n_tasks = 2
    
    # Allocate buffers and initialize done flags
    cdef char* buf = <char *> malloc(buf_total_size)
    for i in range(n_bufs):
        dones[i] = 0
        gots[i] = 0
        total_gots[i] = 0
        offsets[i] = i * buf_size

    # Enables dynamic adjustment of the number of threads 
    openmp.omp_set_dynamic(1)
    cdef int num_threads 
    cdef char* my_buf
    cdef int my_fd
    cdef int my_threadid
    with nogil, parallel(num_threads=n_bufs):
    #for i in range(6):
        num_threads = openmp.omp_get_num_threads()
        my_threadid = threadid()
        #my_threadid = i
        #idx = int(my_threadid / n_tasks)
        idx = my_threadid
        my_fd = fds[idx]
        
        #with gil:
        #    print(f'my threadid={my_threadid} idx={idx} my_fd={my_fd} num_threads={num_threads}')
        
        #if my_threadid % n_tasks == 0:
        if True:
            # Reading thread
            while dones[idx] == 0:
                # Check end of my block 
                if offsets[idx] + read_size > buf_size * (idx + 1):
                    offsets[idx] = 0

                my_buf = buf + offsets[idx]
                gots[idx] = read(my_fd, my_buf, read_size)
                total_gots[idx] += gots[idx]
                if gots[idx] <= 0: 
                    dones[idx] = 1
                else:
                    offsets[idx] += gots[idx]

                #with gil:
                #    print(f'my threadid={my_threadid} got={gots[idx]} offsets={offsets[idx]} done={dones[idx]}')
        #else:
            # computing thread
    
    #for i in range(n_bufs):
    #    print(f'buf[{i}] total={total_gots[i]}')





