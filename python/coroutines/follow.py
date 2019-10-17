# To run the example:
# In another terminal,
# >for i in $(seq 0 1000); do echo $i >> access-log; done
# In this terminal,
# python follow.py

import time
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

logfile = open("access-log")
for line in follow(logfile):
    print(line)
