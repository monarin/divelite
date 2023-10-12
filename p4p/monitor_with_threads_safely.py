from p4p.client.thread import Context
import os, sys, time
import threading
import queue
        

class ExcThread(threading.Thread):

    def __init__(self, bucket):
        threading.Thread.__init__(self)
        self.bucket = bucket

    def run(self):
        print(f'Thread ID {threading.get_native_id()}: in run()') 
        def callback(E):
            print(f'Thread ID {threading.get_native_id()}: in callback {E=}')
        try:
            ctxt = Context('pva', nt=None)
            pvStepDone = 'DAQ:NEH:XPM:7:PART:4:StepDone'
            sub = ctxt.monitor(pvStepDone, callback) #, notify_disconnect=True)
            time.sleep(1)
            sub.close()
            ctxt.close()
            #raise Exception(f'Thread ID {threading.get_native_id()}: An error occured here.')
        except Exception:
            self.bucket.put(sys.exc_info())


def main():
    bucket = queue.Queue()
    threads = []
    n_threads = 10
    for i in range(n_threads):
        threads.append(ExcThread(bucket))
        threads[-1].start()

    print([t.is_alive() for t in threads])
    while True:
        try:
            exc = bucket.get(block=False)
        except queue.Empty:
            print(f'Empty queue')
            pass
        else:
            exc_type, exc_obj, exc_trace = exc
            # deal with the exception
            print(f'Caught this: {exc_type=}, {exc_obj=}', flush=True)
            print(f'Trace Info: {exc_trace=}', flush=True)

        for i in range(n_threads):
            threads[i].join()

        if not any([t.is_alive() for t in threads]):
            break
            

if __name__ == '__main__':
    main()
