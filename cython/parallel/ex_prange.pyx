from cython.parallel import prange
import numpy as np
#from posix.time cimport timeval, gettimeofday
import time


def do_prange(int n, int batch_size):
    cdef int i, j
    cdef int sum_i = 0

    #cdef timeval tv_st, tv_en
    #cdef unsigned long ut_st, ut_en
    cdef double time_st, time_en
    time_st = time.time()
    
    #gettimeofday(&tv_st, NULL)
    for i in prange(n, nogil=True, schedule='static'):
        for j in range(batch_size):
            sum_i += 1
    #gettimeofday(&tv_en, NULL)
    #ut_st = 1000000 * tv_st.tv_sec + tv_st.tv_usec
    #ut_en = 1000000 * tv_en.tv_sec + tv_en.tv_usec
    #print(f'{ut_st} {ut_en} {ut_en - ut_st} {sum_i}')
    time_en = time.time()
    print(f'{time_st} {time_en} {time_en-time_st}')

"""


def func(double[:] x, double alpha):
    cdef Py_ssize_t i

    for i in prange(x.shape[0], nogil=True):
        x[i] = alpha * x[i]


narr = np.arange(100000000, dtype=np.float64)
#cdef int[:] narr_view = narr
func(narr, 0.5)
"""
