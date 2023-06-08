from mypybuffer cimport MyPyBuffer

cdef class MyPyBufferConsumer:
    cdef list pybuffer_list

    cdef __init__(self, views):
        for view in view:
            # Create a new PyBuffer handler and acquire view_ptr
            mpb = MyMyBuffer()
            mpb.get_buffer(view)
            pybuffer_list.add(mpb)
