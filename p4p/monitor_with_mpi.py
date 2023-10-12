from p4p.client.thread import Context
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
        
def get():
    ctxt = Context('pva', nt=None)
    pvStepDone = 'DAQ:NEH:XPM:7:PART:4:StepDone'
    retval = ctxt.get([pvStepDone], throw=False)
    print(pvStepDone, retval)
    ctxt.close()

def monitor():
    def callback(E):
        print(f'in calback {rank=} {E=}')
    ctxt = Context('pva', nt=None)
    pvStepDone = 'DAQ:NEH:XPM:7:PART:4:StepDone'
    sub = ctxt.monitor(pvStepDone, callback, notify_disconnect=True)
    time.sleep(1)
    sub.close()
    ctxt.close()


if __name__ == "__main__":
    print(f'{rank=} start')
    monitor()
