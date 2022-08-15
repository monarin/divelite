# Test that shows PyObject_GetBuffer does copy when called
from mypybuffer import MyPyBuffer
import os

xtc_file = '/cds/home/m/monarin/lcls2/psana/psana/tests/test_data/dgrampy-test.xtc2'
fd = os.open(xtc_file, os.O_RDONLY)
size = 2643928     # size of dgrampy-test.xtc2
view = bytearray(os.read(fd, size))

offset = 0
cn_dgrams = 0
mpb = MyPyBuffer()
while offset < size:
    mpb.get_buffer(view[offset:])

    # To demonstrate that copy happens, we obtained the view ptr from the line
    # above and here we'll replace the content of that view. You'll see that
    # print_dgram() still prints out the old content.
    if cn_dgrams == 1:
        view[offset:] = config_bytes
        
        # Uncomment below to see that we need to call PyObject_GetBuffer again
        # to update view ptr
        #mpb.free_buffer()
        #mpb.get_buffer(view[offset:])

    mpb.print_dgram()

    # Save config so that we can use it to replace the second dgram
    if offset == 0:
        config_bytes = view[: mpb.dgram_size]

    offset += mpb.dgram_size
    cn_dgrams += 1
    
    mpb.free_buffer()

    if cn_dgrams == 2:
        break


