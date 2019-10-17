import multiprocessing as mp
import os
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty # python 2.x

BLOCKSIZE = 0x100000

def f(qfd):
    q, fd = qfd[0], qfd[1]
    for block in nonblocking_read(fd):
        q.put(block, False)

def nonblocking_read(fd):
    while True:
        try:
            block = os.read(fd, BLOCKSIZE)
        except BlockingIOError:
            yield bytearray()  #yield empty buffer if no data
            continue
        
        if not block:
            yield bytearray()
            break

        yield block

def consumer(queue):
    while True:
        try:
            block = queue.get_nowait() # or q.get(timeout=.1)
        except Empty:
            yield bytearray()
            break
        else:
            yield block

def main():
    import glob
    epics_files = glob.glob("/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/smalldata/data-r0001-s*.xtc2")
    epics_fds = [os.open(epics_file, os.O_RDONLY | os.O_NONBLOCK) for epics_file in epics_files]
    p = mp.Pool(processes=len(epics_fds))
    q = mp.Manager().Queue()
    p.map(f, [(q, epics_fd) for epics_fd in epics_fds])

    for block in consumer(q):
        print('received %d bytes'%(memoryview(block).shape[0]))
    
    """    
    its = []
    while True:
        try:
            print("Waiting for item from queue for up to 5 seconds")
            i = q.get(True, 5)
            print("found %d bytes from the queue."%(memoryview(i).shape[0]))
            its.append(i)
        except Empty:
            print("Caught queue empty exception, done")
            break
    print("processed %d items, completion successful"%len(its))
    """

    p.close()
    p.join()


if __name__ == '__main__':
    main()
