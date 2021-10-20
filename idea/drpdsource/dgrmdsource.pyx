from psana.dgram import Dgram
import os

class DgrmDsource:
    """
    Retrieves data from "Drp" (in this case substitute 
    with reading directly from an xtc file) and returns
    Python Dgram object."""
    
    BUFSIZE = 0x4000000
    def __init__(self):
        self.fd = os.open('/cds/home/m/monarin/lcls2/psana/psana/tests/.tmp/data-r0001-s00.xtc2', os.O_RDONLY)

    def __del__(self):
        os.close(self.fd)
        
    def get(self):
        self.buf = os.read(self.fd, self.BUFSIZE)
        print(f"got {memoryview(self.buf).nbytes} bytes")

    def wait_for_drp():
        while True:
            # wait for DRP data
            wait_for_drp(GOT_DATA)
            if GOT_DATA:
                yield evt





