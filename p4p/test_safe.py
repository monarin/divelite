import sys
import threading
import queue


class ExcThread(threading.Thread):

    def __init__(self, bucket):
        threading.Thread.__init__(self)
        self.bucket = bucket

    def run(self):
        try:
            raise Exception(f'Thread ID {threading.get_native_id()}: An error occured here.')
        except Exception:
            self.bucket.put(sys.exc_info())


def main():
    bucket = queue.Queue()
    thread_obj = ExcThread(bucket)
    thread_obj.start()

    t2 = ExcThread(bucket)
    t2.start()

    print([thread_obj.is_alive(), t2.is_alive()])
    while True:
        try:
            exc = bucket.get(block=False)
        except queue.Empty:
            pass
        else:
            exc_type, exc_obj, exc_trace = exc
            # deal with the exception
            print(f'Caught this: {exc_type=}, {exc_obj=}', flush=True)
            print(f'Trackback: {exc_trace=}', flush=True)

        thread_obj.join()
        t2.join()
        
        if not any([thread_obj.is_alive(), t2.is_alive()]):
            break
            

if __name__ == '__main__':
    main()
