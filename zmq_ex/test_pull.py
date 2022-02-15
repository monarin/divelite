""" An example of how to use zmq helper for pulling data.

Requirement: psana1, xtc1to2
    For xtc1to2, 
    git clone git@github.com:monarin/xtc1to2.git
    export PYTHONPATH=/path/to/cloned/loc:$PYTHONPATH
    
"""
import numpy as np
from xtc1to2.socket.zmqhelper import ZmqReceiver

socket = "tcp://127.0.0.1:5557"
zmq_recv = ZmqReceiver(socket)

while True:
    obj = zmq_recv.recv_zipped_pickle()
    if 'done' in obj: break

    print(obj['data'])

