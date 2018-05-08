from collections import deque

from concurrent.futures import Future
# fut = Future()
# fut.result() # blocks - wait for set_result
# other threads
# fut.set_result(42) # unblock

from threading import Thread, Lock

from asyncio import wait_for, wrap_future, get_event_loop

# coroutine checking ex.
import sys
def from_coroutine():
    return sys._getframe(2).f_code.co_flags & 0x380

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
            # Wak a putter
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

    async def get_async(self):
        item, fut = self.get_noblock()
        if fut:
            item = await wait_for(wrap_future(fut), None)
        return item

    def get(self):
        if from_coroutine():
            return self.get_async()
        else: 
            return self.get_sync()
    
    def put_sync(self, item):
        while True: # try to put
            fut = self.put_noblock(item)
            if fut is None:
                return 
            fut.result()

    async def put_async(self, item):
        while True:
            fut = self.put_noblock(item)
            if fut is None:
                return
            await wait_for(wrap_future(fut), None)

    def put(self, item):
        if from_coroutine():
            return self.put_async(item)
        else:
            return self.put_sync(item)


def producer(q, n):
    for i in range(n):
        q.put(i)
    q.put(None)

async def aproducer(q, n):
    for i in range(n):
        await q.put(i)
    await q.put(None)

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break

        print("Got:", item)

async def aconsumer(q):
    while True:
        item = await q.get()
        if item is None:
            break

        print("Async Got:", item)

# ex1 thread producer and async consumer
q = Queuey(2)
Thread(target=producer, args=(q, 10)).start()
loop = get_event_loop()
loop.run_until_complete(aconsumer(q))

# ex2 thread consumer and async producer
q = Queuey(2)
Thread(target=consumer, args=(q,)).start()
loop.run_until_complete(aproducer(q, 10))

from queue import Queue
q = Queue()
Thread(target=producer, args=(q,10)).start()
Thread(target=consumer, args=(q,)).start()

from asyncio import Queue
q = Queue()
loop.create_task(aconsumer(q))
loop.run_until_complete(aproducer(q,10))
