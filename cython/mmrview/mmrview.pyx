from cython.view cimport array as cvarray
import numpy as np
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

# Memoryview on Numpy array
narr = np.arange(27, dtype=np.dtype("i")).reshape((3,3,3))
cdef int [:,:,:] narr_view = narr

# Memoryview on a C array
cdef int carr[3][3][3]
cdef int [:, :, :] carr_view = carr

# Memoryview on a Cython array
cyarr = cvarray(shape=(3,3,3), itemsize=sizeof(int), format="i")
cdef int [:,:,:] cyarr_view = cyarr

# Show the sum of all the arrays before altering it
print("NumPy sum of the NumPy array before assignments: %s" % narr.sum())

# We can copy the values from one memoryview into another using a single
# statement, by either indexing with ... or (NumPy-style) with a colon.
carr_view[...] = narr_view
cyarr_view[:] = narr_view
# NumPy-style syntax for assigning a single value to all elements.
narr_view[:,:,:] = 3

# Just to distinguish the arrays
carr_view[0, 0, 0] = 100
cyarr_view[0, 0, 0] = 1000

# Assigning into the memoryview on the NumPy array alters the latter
print("NumPy sum of NumPy array after assignments: %s" % narr.sum())

# A function using a memoryview does not usually need the GIL
cpdef int sum3d(int[:, :, :] arr) nogil:
    cdef size_t i, j, k
    cdef int total = 0
    I = arr.shape[0]
    J = arr.shape[1]
    K = arr.shape[2]
    for i in range(I):
        for j in range(J):
            for k in range(K):
                total += arr[i, j, k]
    return total

# A function accepting a memoryview knows how to use a NumPy array,
# a C array, a Cython array...
print("Memoryview sum of NumPy array is %s" % sum3d(narr))
print("Memoryview sum of C array is %s" % sum3d(carr))
print("Memoryview sum of Cython array is %s" % sum3d(cyarr))
# ... and of course, a memoryview.
print("Memoryview sum of C memoryview is %s" % sum3d(carr_view))

# Memroyview on char*
CHUNK_SIZE = 0x100000
cdef char *chunk 
chunk = <char *>malloc(CHUNK_SIZE)
cdef char[:] chunk_view = <char[:CHUNK_SIZE]>chunk

# Manipulate char* memory through view and copy to bytearray
chunk_bytearray = bytearray()
chunk_view[:] = b'b'
chunk_bytearray.extend(chunk_view[:4])
print('\nchar pointer, memoryview, and bytearray')
print('chunk', memoryview(<char [:4]>chunk).tobytes())
print('chunk_view', memoryview(chunk_view[:4]).tobytes())
print('chunk_bytearray', chunk_bytearray)

# Some usage of the char* and its memoryview
cdef int from_int = 5
memcpy(chunk, &from_int, sizeof(from_int))
cdef int to_int = 0
memcpy(&to_int, chunk, sizeof(from_int))

# memcpy from a variable to carray
cdef char batch_arr[2][1000]
cdef int i,j
for i in range(2):
    for j in range(3):
        from_int = i * 10 + j
        memcpy(batch_arr[i] + j * sizeof(from_int), &from_int, sizeof(from_int))
        memcpy(&to_int, batch_arr[i] + j * sizeof(from_int), sizeof(from_int))
        #print(i, j, to_int)

# memoryview and its object share the same content
b_array = bytearray(b'abcd')
b_view = memoryview(b_array)
print('\nbytearray and memoryview')
print('b_array', b_array)
print('b_view', b_view.tobytes())
for i in range(2):
    batch_arr[i][:4] = b_array
    #print(batch_arr[i][:b_view.nbytes])

# changing the object changes the memoryview
print('change b_array to defg')
b_array[:] = b'defg'
print('b_array', b_array)
print('b_view', b_view.tobytes())
for i in range(2):
    pass#print(batch_arr[i][:b_view.nbytes])

# changing the view also changes the object
print('copy b2_view to b_view')
b2_array = bytearray(b'hijk')
b2_view = memoryview(b2_array)
b_view[:] = b2_view
print('b_array', b_array)
print('b_view', b_view.tobytes())


# making bytearray or memoryview accessible by a pointer
from cpython.buffer cimport PyObject_GetBuffer, PyBuffer_Release, PyBUF_ANY_CONTIGUOUS, PyBUF_SIMPLE
c_array = bytearray(b'abcd')
print('\nmaking bytearray or memoryview accessible by a pointer')
print(c_array)
c_view = memoryview(c_array)
cdef Py_buffer buf
cdef list c_list = [0]
cdef char[:] c_to_view
cdef char* c_ptr

# Fill buf with c_view's buffer and increase refcount by one - this is doing copying
PyObject_GetBuffer(c_view, &buf, PyBUF_SIMPLE | PyBUF_ANY_CONTIGUOUS)
c_ptr = <char *>buf.buf
c_to_view = <char [:4]>c_ptr
c_list[0] = c_to_view

c_to_view = bytearray(b'defg')
print('after change')
print('c_array', c_array)
print('c_view', c_view.tobytes())
print('c_to_view', memoryview(c_to_view).tobytes())
print('memoryview of c_list[0]', memoryview(c_list[0]).tobytes())


