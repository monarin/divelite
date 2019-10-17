from collections import deque

class Queuey:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.items = deque()

    def get(self):
        return self.items.popleft()

    def put(self, item):
        if len(self.items) < self.maxsize:
            self.items.append(item)
        else:
            print("no")

def producer(q, n):
    for i in range(n):
        q.put(i)
    q.put(None)

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break

        print("Got:", item)

from threading import Thread
from queue import Queue
q = Queue()
Thread(target=producer, args=(q,100)).start()
Thread(target=consumer, args=(q,)).start()
