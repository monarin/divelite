from collections import deque

from concurrent.futures import Future
# fut = Future()
# fut.result() # blocks - wait for set_result
# other threads
# fut.set_result(42) # unblock

class Queuey:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.items = deque()
        self.getters = deque()
        self.putters = deque()

    def get_noblock(self):
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

if __name__ == "__main__":
    q = Queuey(2)
    q.put_noblock(1)
    q.put_noblock(2)
    print(q.put_noblock(3)) # q is full
    print(q.items)
    print(q.putters)

    q.get_noblock() # free up an item in the q
    print(q.putters)

    q.get_noblock() 
    a = q.get_noblock() # nothing more to get -->wait

    print(a)
    q.put_noblock(3)
    print(a)
    print(a[1].result())
