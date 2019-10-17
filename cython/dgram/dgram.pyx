from cython.view cimport array as cvarray
from cpython.buffer cimport PyObject_GetBuffer, PyBuffer_Release, PyBUF_ANY_CONTIGUOUS, PyBUF_SIMPLE
from libc.string cimport memcpy

cdef struct Xtc:
    int junks[2]
    unsigned extent

cdef struct Sequence:
    int junks[2]
    unsigned low
    unsigned high

cdef struct Dgram:
    Sequence seq
    unsigned env
    Xtc xtc

def get(data):
    cdef Py_buffer view
    cdef char* c_ptr
    cdef Dgram* d
    cdef list dgrams = [0]
    cdef char batch_arr[2][100000]

    # Fill buf with c_view's buffer and increase refcount by one
    PyObject_GetBuffer(data, &view, PyBUF_SIMPLE | PyBUF_ANY_CONTIGUOUS)
    c_ptr = <char *>view.buf
    d = <Dgram*>c_ptr
    payload = d.xtc.extent - sizeof(Xtc)
    dgrams[0] = <char [:sizeof(Dgram)+payload]>c_ptr
    batch_arr[0][:sizeof(Dgram)+payload] = bytearray(dgrams[0])
    PyBuffer_Release(&view)


