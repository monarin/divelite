from time import sleep
from queue import Queue
from threading import Thread

def producer(q, n):
    for i in range(n):
        q.put(i)
        sleep(5)
    q.put(None)

def consumer(q):
    while True:
        print("Wait...")
        item = q.get()
        if item is None:
            break

        print("Got:", item)


q = Queue()
Thread(target=producer, args=(q,10)).start()
Thread(target=consumer, args=(q,)).start()
