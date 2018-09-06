from queue import Queue
from threading import Thread
from time import sleep

q = Queue(2)
print(q.empty())
q.put(1)
q.put(2)
print(q.get())
print(q.get())

Thread(target=lambda:(sleep(10), q.put(42))).start()
print(q.get())

# q is blocking



