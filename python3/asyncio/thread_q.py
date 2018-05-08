from collections import deque

from concurrent.futures import Future
# fut = Future()
# fut.result() # blocks - wait for set_result
# other threads
# fut.set_result(42) # unblock

from threading import Thread, Lock

from time import sleep

class Queuey:
    def __init__(self, maxsize):
        self.mutex = Lock()
        self.maxsize = maxsize
        self.items = deque()
        self.getters = deque()
        self.putters = deque()

    def get_noblock(self):
      with self.mutex:
        if self.items:
            # Wake a putter
            if self.putters:
                self.putters.popleft().set_result(True)
            return self.items.popleft(), None
        else:
            fut = Future()
            self.getters.append(fut)
            return None, fut

    def put_noblock(self, item):
      with self.mutex:
        if len(self.items) < self.maxsize:
            self.items.append(item)
            # Wake a getter
            if self.getters:
                self.getters.popleft().set_result(
                        self.items.popleft())
        else:
            fut = Future()
            self.putters.append(fut)
            return fut

    def get_sync(self):
        item, fut = self.get_noblock()
        if fut:
            item = fut.result() # wait for it
        return item

    def put_sync(self, item):
        while True: # try to put
            fut = self.put_noblock(item)
            if fut is None:
                return 
            fut.result()

def producer(q, n):
    for i in range(n):
        q.put_sync(i)
    q.put_sync(None)

def consumer(q):
    while True:
        item = q.get_sync()
        if item is None:
            break

        print("Got:", item)

if __name__ == "__main__":
    q = Queuey(2)
    Thread(target=producer, args=(q, 10)).start()
    Thread(target=consumer, args=(q,)).start()
