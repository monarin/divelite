import sys
import numpy as np
import matplotlib.pyplot as plt

log_fname = sys.argv[1]
size = int(sys.argv[2])

data = {}
with open(log_fname) as f:
    for line in f:
        cols = line.split()
        if len(cols) == 2:
            rank = int(cols[0])
            ts = float(cols[1])
            if rank not in data:
                data[rank] = [ts]
            else:
                data[rank].append(ts)

deltas = []
for i in range(1, size):
    if i in data:
        plt.scatter([i]*len(data[i]), data[i], s=2, marker='o')
        # calculate delta
        ts_list = data[i]
        for j in range(len(ts_list)-1):
            deltas.append(ts_list[j+1] - ts_list[j])

plt.show()

# plot histogram of deltas
deltas = np.asarray(deltas)
plt.hist(deltas, bins=100)
plt.title("No. points %d More than 0.5s %d Min %f Max %f Mean %f"%(deltas.size, deltas[deltas>0.5].size, np.min(deltas), np.max(deltas), np.average(deltas)))
plt.show()
