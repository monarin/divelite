from cython.parallel import prange

def run():
    cdef int i
    cdef int n = 5
    cdef int sum = 0
    cdef int cn = 0

    for i in prange(n, nogil=True):
        if i == n:
            cn += 1
        else:
            sum += i

    print(cn, sum)
