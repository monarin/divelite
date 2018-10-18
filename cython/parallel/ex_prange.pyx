from cython.parallel import prange
import numpy as np
cdef int i
cdef int n = 1000
cdef int sum = 0

for i in prange(n, nogil=True):
#for i in range(n):
    sum += i

print(sum)
"""


def func(double[:] x, double alpha):
    cdef Py_ssize_t i

    for i in prange(x.shape[0], nogil=True):
        x[i] = alpha * x[i]


narr = np.arange(100000000, dtype=np.float64)
#cdef int[:] narr_view = narr
func(narr, 0.5)
"""
