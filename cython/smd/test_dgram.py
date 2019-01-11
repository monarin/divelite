from psana import dgram
import os
import time

fd = os.open("/ffb01/monarin/hsd/data-r0001-s00.xtc", os.O_RDONLY)
config = dgram.Dgram(file_descriptor=fd)

limits = 1000
for i in range(limits):
    #st = time.time()
    d = dgram.Dgram(config=config)
    #en = time.time()
    #print(en-st)
