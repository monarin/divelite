import time
from p4p.nt import NTScalar
from p4p.server import Server
from p4p.server.thread import SharedPV

pv = SharedPV(nt=NTScalar('d'), # scalar double
              initial=0.5)      # setting initial value also open()'s
@pv.put
def handle(pv, op):
    pv.post(op.value()) # just store and update subscribers
    op.done()

Server.forever(providers=[{
    'demo:pv:name':pv, # PV name only appears here
}]) # runs until KeyboardInterrupt
