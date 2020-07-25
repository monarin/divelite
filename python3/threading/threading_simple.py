import threading
import time

def worker():
    while True:
        print('Worker')
        time.sleep(1)
    return

threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
