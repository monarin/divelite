from cpython.buffer cimport PyObject_GetBuffer, PyBuffer_Release, PyBUF_ANY_CONTIGUOUS, PyBUF_SIMPLE
from libc.stdint cimport uint32_t, uint64_t

cdef struct Xtc:
    int junks[2]
    uint32_t extent

cdef struct Sequence:
    uint32_t low
    uint32_t high

cdef struct Dgram:
    Sequence seq
    uint32_t env
    Xtc xtc

cdef class MyPyBuffer:
    cdef Py_buffer buf
    cdef char* view_ptr
    cdef uint64_t dgram_size

    def __init__(self):
        pass

    def get_buffer(self, view):
        PyObject_GetBuffer(view, &(self.buf), PyBUF_SIMPLE | PyBUF_ANY_CONTIGUOUS)
        self.view_ptr = <char *>self.buf.buf

    def print_dgram(self):
        cdef Dgram* d = <Dgram *>(self.view_ptr)
        cdef uint64_t payload = d.xtc.extent - sizeof(Xtc)
        cdef uint64_t ts = <uint64_t>d.seq.high << 32 | d.seq.low
        cdef uint32_t service = (d.env>>24)&0xf
        self.dgram_size = sizeof(Dgram) + payload
        print(f'ts={ts} service={service} payload={payload}')

    def free_buffer(self):
        PyBuffer_Release(&(self.buf))

    @property
    def dgram_size(self):
        return self.dgram_size
