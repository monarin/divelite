"""
test_push.py and test_pull.py tests Pipeline pattern of zmq 
"""
import numpy as np
from xtc1to2.socket.zmqhelper import ZmqSender

socket = "tcp://127.0.0.1:5557"
zmq_send = ZmqSender(socket)

data = {'data': np.array([1.01, 1e+9, 1e-9], dtype=np.double)}
zmq_send.send_zipped_pickle(data)

done_dict = {'done': True}
zmq_send.send_zipped_pickle(done_dict)

