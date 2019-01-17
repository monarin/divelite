import sys
import numpy as np
import matplotlib.pyplot as plt

size = int(sys.argv[1])

data = {}
with open('xx') as f:
    for line in f:
        cols = line.split()
        if len(cols) == 2:
            rank = int(cols[0])
            ts = float(cols[1])
            if rank not in data:
                data[rank] = [ts]
            else:
                data[rank].append(ts)

for i in range(1, size):
    if i in data:
        plt.scatter([i]*len(data[i]), data[i], s=2, marker='o')

plt.show()


