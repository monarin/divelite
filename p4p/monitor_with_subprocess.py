from p4p.client.thread import Context
import time
import os, sys
import subprocess
        
def monitor():
    def callback(E):
        print(f'in calback {E=}')
    ctxt = Context('pva', nt=None)
    #pvStepDone = 'DAQ:NEH:XPM:7:PART:4:StepDone'
    pvDemo = 'demo:pv:name'
    sub = ctxt.monitor(pvDemo, callback) #, notify_disconnect=True)
    time.sleep(1)
    sub.close()
    ctxt.close()
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        monitor()
    else:
        try:
            complete_proc = subprocess.run(["python", __file__, "monitor"], capture_output=True)
        except subprocess.CalledProcessError as e:
            complete_proc = e
        print(f'{complete_proc.stdout=}')
        print(f'{complete_proc.stderr=}')
        print(f'{complete_proc.returncode=}')
