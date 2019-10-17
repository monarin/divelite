import sys, os, fcntl, locale
from threading import Thread

try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty # python 2.x

def enqueue_output(f, queue):
    for line in nonblocking_readlines(f):
        queue.put(line)

def nonblocking_readlines(f):
    fd = f.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    enc = locale.getpreferredencoding(False)

    buf = bytearray()
    while True:
        try:
            block = os.read(fd, 8192)
        except BlockingIOError:
            yield ""  #yield empty string if no data
            continue

        if not block:
            if buf:
                yield buf.decode(enc)
                buf.clear()
            break

        buf.extend(block)

        while True:
            r = buf.find(b'\r')
            n = buf.find(b'\n')
            if r == -1 and n == -1: break

            if r == -1 or r > n:
                yield buf[:(n+1)].decode(enc)
                buf = buf[(n+1):]
            elif n == -1 or n > r:
                yield buf[:r].decode(enc) + '\n'
                if n == r+1:
                    buf = buf[(r+2):]
                else:
                    buf = buf[(r+1):]

def consumer(queue):
    while True:
        try:
            line = queue.get_nowait() # or q.get(timeout=.1)
        except Empty:
            pass#print('no output yet')
        else:
            print('got line', line)
        

f = open('dummy.txt', 'r')
q = Queue()
t = Thread(target=enqueue_output, args=(f, q)).start()

t2 = Thread(target=consumer, args=(q, )).start()




