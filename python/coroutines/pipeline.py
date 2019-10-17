# In another terminal,
# >for i in $(seq 0 1000); do mymod=$(expr $i % 10); if [ "$mymod" -eq 0 ]; then echo $i python >> access-log; else echo $i >> access-log; fi; done
# then run python pipeline.py

import time
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line

# Set up a processing pipe: tail -f | grep python
logfile = open("access-log")
loglines = follow(logfile)
pylines = grep("python", loglines)

# Pull results out of the processing pipeline
for line in pylines:
    print(line)
