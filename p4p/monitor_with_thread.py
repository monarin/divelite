from p4p.client.thread import Context
import time
from threading import Thread, Event, Condition
import threading
import os
        
def get():
    ctxt = Context('pva', nt=None)
    pvStepDone = 'DAQ:NEH:XPM:7:PART:4:StepDone'
    retval = ctxt.get([pvStepDone], throw=False)
    print(pvStepDone, retval)
    ctxt.close()

def monitor(ctxt):
    def callback(E):
        print(f'in calback ID:{threading.get_native_id()} {E=}')
    pvName = 'DAQ:NEH:XPM:7:PART:4:StepDone'
    #pvName = 'demo:pv:name'
    sub = ctxt.monitor(pvName, callback) #, notify_disconnect=True)
    time.sleep(1)
    sub.close()
    
def monitor_local():
    def callback(E):
        print(f'in calback ID:{threading.get_native_id()} {E=}')
    ctxt = Context('pva', nt=None)
    pvName = 'DAQ:NEH:XPM:7:PART:4:StepDone'
    #pvName = 'demo:pv:name'
    sub = ctxt.monitor(pvName, callback) #, notify_disconnect=True)
    time.sleep(1)
    sub.close()
    ctxt.close()

if __name__ == "__main__":
    n_threads = 10
    t_list = [None for i in range(n_threads)] 
    #ctxt = Context('pva', nt=None)
    for i in range(n_threads):
        #t_list[i] = Thread(target=monitor, args=(ctxt,), name='stepdone')
        t_list[i] = Thread(target=monitor_local, name='stepdone')
        t_list[i].start()
    
    for i in range(n_threads):
        t_list[i].join()
    #ctxt.close()
