from libc.stdlib cimport malloc, free

ctypedef struct my_c_struct:
    int a
    int b

cdef class MyClass:
    cdef int a
    cdef int b
    cdef void *_ptr
    cdef bint ptr_owner

    def __cinit__(self):
        self.ptr_owner = False
        self.a = 0
        self.b = 0

    def __dealloc__(self):
        if self._ptr is not NULL and self.ptr_owner is True:
            free(self._ptr)
            self._ptr = NULL
    
    @staticmethod
    cdef MyClass from_ptr(void *_ptr, bint owner=False):
        cdef MyClass myc = MyClass.__new__(MyClass)
        myc._ptr = _ptr
        myc.ptr_owner = owner
        return myc

    @staticmethod
    cdef MyClass new_class():
        cdef MyClass *_ptr = MyClass.__new__(MyClass)
        if _ptr is NULL:
            raise MemoryError
        _ptr.a = 0
        _ptr.b = 0
        return MyClass.from_ptr(_ptr, owner=True)

cdef class WrapperClass:
    cdef void *_ptr
    cdef bint ptr_owner

    def __cinit__(self):
        self.ptr_owner = False

    def __dealloc__(self):
        if self._ptr is not NULL and self.ptr_owner is True:
            free(self._ptr)
            self._ptr = NULL

    # Extension class properties
    @property
    def a(self):
        return self._ptr.a if self._ptr is not NULL else None

    @property
    def b(self):
        return self._ptr.b if self._ptr is not NULL else None

    @staticmethod
    cdef WrapperClass from_ptr(void *_ptr, bint owner=False):
        """Factory function fo create WrapperClass objects from
        given my_c_struct pointer.

        Setting owner flag to True causes
        the extension type to free the structure pointed to by _ptr
        when the wrapper object is deallocated."""
        # Call to __new__ bypasses __init__ contstructor
        cdef WrapperClass wrapper = WrapperClass.__new__(WrapperClass)
        wrapper._ptr = _ptr
        wrapper.ptr_owner = owner
        return wrapper

    @staticmethod
    cdef WrapperClass new_class():
        """Factory function to create WrapperClass objects with
        newly allocated my_c_struct"""
        cdef MyClass *_ptr = MyClass.new_class()
        if _ptr is NULL:
            raise MemoryError
        _ptr.a = 0
        _ptr.b = 0
        return WrapperClass.from_ptr(_ptr, owner=True)

def test():
    cdef MyClass *mycs = MyClass.new_class()
    mycs.a = 1
    mycs.b = 2
    cdef wrapc = WrapperClass.from_ptr(mycs)
    print(wrapc.a, wrapc.b)
