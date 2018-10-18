from cython.parallel import parallel, prange
from libc.stdlib cimport abort, malloc, free

cdef Py_ssize_t idx, i
cdef int * local_buf
cdef size_t size = 10

cdef inline void func(int* local_buf) nogil:
    local_buf[0] = 0
    
cdef int sum = 0
with nogil, parallel():
    local_buf = <int *> malloc(sizeof(int) * size)
    if local_buf is NULL:
        abort()

    # populate our local buffer in a sequential loop
    for i in xrange(size):
        local_buf[i] = i * 2

    # share the work using the thread-local buffer(s)
    for idx in prange(size, schedule='guided'):
        sum += local_buf[idx]

    free(local_buf)

print(sum)
