from multiprocessing import Pool
import signal, os, time

def f(x):
    print('hello',x)
    return x*2

if __name__ == '__main__':
    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    p = Pool(5)
    signal.signal(signal.SIGINT, original_sigint_handler)
    try:
        res = p.map_async(f, range(10000000))
        print("Waiting for results")
        res.get(60)
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        p.terminate()
    else:
        print("Normal termination")
        p.close()
    p.join()
    
