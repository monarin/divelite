import dgram
from psana import dgram as psana_dgram
from psana.smdreader import SmdReader
import os

fd = os.open('data-r0001-s00.smd.xtc2', os.O_RDONLY)
config = psana_dgram.Dgram(file_descriptor=fd)
smdr = SmdReader([fd])
smdr.get(1)
print(smdr.got_events)
dgram.get(smdr.view(0))

